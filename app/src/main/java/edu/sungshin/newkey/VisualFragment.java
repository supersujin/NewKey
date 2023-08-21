package edu.sungshin.newkey;

import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.ImageRequest;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;

import java.util.ArrayList;

public class VisualFragment extends Fragment {
    RequestQueue queue;
    ImageView imageView;
    ArrayList<RankItem> newsList;
    String imageUrl = "http://18.233.147.47:5000/wordsImage";
    String listUrl = "http://18.233.147.47:5000/wordsList";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView=(ViewGroup) inflater.inflate(R.layout.fragment_visual, container, false);

        queue = Volley.newRequestQueue(rootView.getContext());
        imageView=rootView.findViewById(R.id.imageView);
        newsList=new ArrayList<RankItem>();

        final JsonArrayRequest listRequest=new JsonArrayRequest(Request.Method.GET, listUrl, null, new Response.Listener<JSONArray>() {
            @Override
            public void onResponse(JSONArray response) {
                try {
                    for (int i = 0; i < response.length(); i++) {
                        String item=response.getString(i);
                        System.out.println(item);
                        RankItem rankItem = new RankItem(Integer.toString(i+1),item); //i+1: rank
                        newsList.add(rankItem);
                    }
                    LinearLayoutManager layoutManager=new LinearLayoutManager(getContext(),LinearLayoutManager.VERTICAL,false);
                    RecyclerView recyclerView=rootView.findViewById(R.id.recyclerView);
                    recyclerView.setLayoutManager(layoutManager);
                    RankAdapter adapter=new RankAdapter(rootView.getContext(),newsList);
                    recyclerView.setAdapter(adapter);

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println(error);
            }
        });

        listRequest.setRetryPolicy(new DefaultRetryPolicy(
                100000000,  // 기본 타임아웃 (기본값: 2500ms)
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES, // 기본 재시도 횟수 (기본값: 1)
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        final ImageRequest imageRequest = new ImageRequest(imageUrl, new Response.Listener<Bitmap>() {
            @Override
            public void onResponse(Bitmap response) {
                Log.d("test","image get");
                imageView.setImageBitmap(response);

                listRequest.setShouldCache(false);
                queue.add(listRequest);
            }
        },
        500, 500, ImageView.ScaleType.CENTER_CROP, null, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                // 에러 처리
                System.out.println(error);
            }
        });

        imageRequest.setRetryPolicy(new DefaultRetryPolicy(
                100000000,  // 기본 타임아웃 (기본값: 2500ms)
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES, // 기본 재시도 횟수 (기본값: 1)
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        imageRequest.setShouldCache(false);
        queue.add(imageRequest);

        return rootView;
    }
}
