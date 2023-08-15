package edu.sungshin.newkey;

import android.graphics.Bitmap;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.ImageRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.HashMap;
import java.util.Map;

public class NewsFragment extends Fragment {

    RequestQueue queue;
    ImageView imageView;
    TextView fiveWOneH;
    TextView title;
    TextView content;
    String imageUrl;
    String fiveWOneHUrl="http://44.212.55.152:5000/5w1h";
    NewsData newsData;

    // 기본 생성자 (반드시 필요)
    public NewsFragment() {
    }

    // NewsData를 전달받는 생성자
    public NewsFragment(NewsData newsData) {
        this.newsData = newsData;
    }

    // Fragment에서 사용할 정보 getter 메서드
    public NewsData getNewsData() {
        return newsData;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView=(ViewGroup) inflater.inflate(R.layout.fragment_news, container, false);

        fiveWOneH=rootView.findViewById(R.id.fiveWOneH);
        title=rootView.findViewById(R.id.newsTitle);
        content=rootView.findViewById(R.id.newsContent);
        imageView=rootView.findViewById(R.id.imageView);
        queue=Volley.newRequestQueue(rootView.getContext());

        title.setText(newsData.getTitle());
        content.setText(newsData.getContent());
        imageUrl= newsData.getImg();

        final StringRequest fiveWOneHRequest=new StringRequest(Request.Method.POST, fiveWOneHUrl, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                fiveWOneH.setText(response);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println(error);
            }
        }){
            //@Nullable
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String, String> params = new HashMap<>();
                params.put("summary",newsData.getSummary());
                params.put("key",newsData.getKey());
                return params;
            }
        };

        fiveWOneHRequest.setRetryPolicy(new DefaultRetryPolicy(
                100000000,  // 기본 타임아웃 (기본값: 2500ms)
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES, // 기본 재시도 횟수 (기본값: 1)
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        final ImageRequest imageRequest = new ImageRequest(imageUrl, new Response.Listener<Bitmap>() {
            @Override
            public void onResponse(Bitmap response) {
                Log.d("test","image get");
                try {
                    imageView.setImageBitmap(response);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                fiveWOneHRequest.setShouldCache(false);
                queue.add(fiveWOneHRequest);
            }
        },
                500, 500, ImageView.ScaleType.CENTER_CROP, null, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                // 에러 처리
                System.out.println(error);
                fiveWOneHRequest.setShouldCache(false);
                queue.add(fiveWOneHRequest);
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