package edu.sungshin.newkey;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SelCatFragment extends Fragment {

    String url="http://44.212.55.152:5000/selCat";
    ArrayList<SelCat> selCatList;
    RequestQueue queue;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView=(ViewGroup) inflater.inflate(R.layout.fragment_sel_cat, container, false);

        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        String userId = user.getUid();
        selCatList=new ArrayList<>();
        queue = Volley.newRequestQueue(rootView.getContext());

        final StringRequest request=new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.d("res",response);

                Type listType = new TypeToken<ArrayList<Integer>>(){}.getType();
                ArrayList<Integer> intSelCatList = new Gson().fromJson(response, listType);

                for (int i = 0; i < intSelCatList.size(); i++) {
                    // selCat 클래스를 사용하여 데이터를 저장하고 리스트에 추가
                    Integer intCat=intSelCatList.get(i);
                    String strCat="";

                    if(intCat.equals(100264)) strCat="대통령실";


                    SelCat selCat = new SelCat(strCat);
                    selCatList.add(selCat);

                    // 이후에 selCatList를 사용하여 원하는 처리를 진행
                    //Adapter
                    LinearLayoutManager layoutManager=new LinearLayoutManager(getContext(),LinearLayoutManager.VERTICAL,false);
                    RecyclerView recyclerView=rootView.findViewById(R.id.recyclerView);
                    recyclerView.setLayoutManager(layoutManager);
                    SelCatAdapter adapter=new SelCatAdapter(rootView.getContext(),selCatList);
                    recyclerView.setAdapter(adapter);
                }
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
                params.put("user_id", userId); // 로그인 아이디로 바꾸기
                return params;
            }
        };

        request.setShouldCache(false);
        queue.add(request);

        return rootView;
    }
}