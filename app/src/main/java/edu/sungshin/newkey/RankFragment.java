package edu.sungshin.newkey;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class RankFragment extends Fragment {
    RankItem rankItem;

    String url = "http://44.212.55.152:5000/keyword";

    ArrayList<NewsData> newsList;
    RequestQueue queue;
    String keyword;

    public RankFragment() {
    }

    public RankFragment(RankItem rankItem) {
        this.rankItem = rankItem;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView = (ViewGroup) inflater.inflate(R.layout.fragment_rank, container, false);
        keyword = rankItem.getContent();

        newsList = new ArrayList<>();
        queue = Volley.newRequestQueue(rootView.getContext());

        // RecyclerView와 어댑터 초기화
        LinearLayoutManager layoutManager = new LinearLayoutManager(getContext(), LinearLayoutManager.VERTICAL, false);
        RecyclerView recyclerView = rootView.findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(layoutManager);
        NewsAdapter adapter = new NewsAdapter(rootView.getContext(), newsList);
        recyclerView.setAdapter(adapter);

        final StringRequest request = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONArray jsonArray = new JSONArray(response);

                    for (int i = 0; i < jsonArray.length(); i++) {
                        JSONObject jsonObject = jsonArray.getJSONObject(i);
                        String id = jsonObject.getString("id");
                        String title = jsonObject.getString("title");
                        String content = jsonObject.getString("content");
                        String press = jsonObject.getString("media");
                        String date = jsonObject.getString("date");

                        NewsData newsData = new NewsData(id, title, content, press, date);
                        newsList.add(newsData);
                    }

                    adapter.notifyDataSetChanged(); // 데이터 변경 알림
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println(error);
            }
        }) {
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String, String> params = new HashMap<>();
                params.put("keyword", keyword);
                return params;
            }
        };

        request.setShouldCache(false);
        queue.add(request);

        return rootView;
    }
}
