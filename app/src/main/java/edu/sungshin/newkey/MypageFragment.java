package edu.sungshin.newkey;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import org.json.JSONArray;

public class MypageFragment extends Fragment {
    TextView email;
    Button selCat,viewNews,logout,withdrawal;
    String selCatUrl="http://44.212.55.152:5000/selCat";
    String viewNewsUrl="http://44.212.55.152:5000/viewNews";

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView=(ViewGroup) inflater.inflate(R.layout.fragment_mypage, container, false);
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        String userId = user.getUid();

        email=rootView.findViewById(R.id.userid);
        selCat=rootView.findViewById(R.id.sel_cat);
        viewNews=rootView.findViewById(R.id.view_news);
        logout=rootView.findViewById(R.id.logout);
        withdrawal=rootView.findViewById(R.id.withdrawal);

        //userId 서버로 전달
        selCat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /*
                //다른 화면으로 이동 후 아래 코드 실행
                final JsonArrayRequest listRequest=new JsonArrayRequest(Request.Method.GET, listUrl, null, new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            for (int i = 0; i < response.length(); i++) {
                                String item=response.getString(i);
                                System.out.println(item);
                                newsList.add();
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
                 */
            }
        });

        viewNews.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

            }
        });

        return rootView;
    }
}
