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

    String url="http://18.233.147.47:5000/selCat";
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

                    if(intCat.equals(100264)) strCat="대통령실"; if(intCat.equals(100265)) strCat="국회/정당"; if(intCat.equals(100268)) strCat="북한"; if(intCat.equals(100266)) strCat="행정"; if(intCat.equals(100267)) strCat="국방/외교"; if(intCat.equals(100269)) strCat="정치일반";
                    if(intCat.equals(101259)) strCat="금융"; if(intCat.equals(101258)) strCat="증권"; if(intCat.equals(101261)) strCat="산업/재계"; if(intCat.equals(101771)) strCat="중기/벤처"; if(intCat.equals(101260)) strCat="부동산"; if(intCat.equals(101262)) strCat="글로벌 경제"; if(intCat.equals(101310)) strCat="생활경제"; if(intCat.equals(101263)) strCat="경제일반";
                    if(intCat.equals(102249)) strCat="사건사고"; if(intCat.equals(102250)) strCat="교육"; if(intCat.equals(102251)) strCat="노동"; if(intCat.equals(102254)) strCat="언론"; if(intCat.equals(102252)) strCat="환경"; if(intCat.equals(102596)) strCat="인권/복지"; if(intCat.equals(102255)) strCat="식품/의료"; if(intCat.equals(102256)) strCat="지역"; if(intCat.equals(102276)) strCat="인물"; if(intCat.equals(102257)) strCat="사회일반";
                    if(intCat.equals(103241)) strCat="건강정보"; if(intCat.equals(103239)) strCat="자동차/시승기"; if(intCat.equals(103240)) strCat="도로/교통"; if(intCat.equals(103237)) strCat="여행/레저"; if(intCat.equals(103238)) strCat="음식/맛집"; if(intCat.equals(103376)) strCat="패션/뷰티"; if(intCat.equals(103242)) strCat="공연/전시"; if(intCat.equals(103243)) strCat="책"; if(intCat.equals(103244)) strCat="종교"; if(intCat.equals(103248)) strCat="날씨"; if(intCat.equals(103245)) strCat="생활문화 일반";
                    if(intCat.equals(104231)) strCat="아시아/호주"; if(intCat.equals(104232)) strCat="미국/중남미"; if(intCat.equals(104233)) strCat="유럽"; if(intCat.equals(104234)) strCat="중동/아프리카"; if(intCat.equals(104322)) strCat="세계일반";
                    if(intCat.equals(105731)) strCat="모바일"; if(intCat.equals(105226)) strCat="인터넷/SNS"; if(intCat.equals(105227)) strCat="통신/뉴미디어"; if(intCat.equals(105230)) strCat="IT일반"; if(intCat.equals(105732)) strCat="보안/해킹"; if(intCat.equals(105283)) strCat="컴퓨터"; if(intCat.equals(105229)) strCat="게임/리뷰"; if(intCat.equals(105228)) strCat="과학일반";
                    if(intCat.equals(110111)) strCat="연재"; if(intCat.equals(110112)) strCat="칼럼"; if(intCat.equals(110113)) strCat="사설";
                    if(intCat.equals(120121)) strCat="야구"; if(intCat.equals(120122)) strCat="해외야구"; if(intCat.equals(120123)) strCat="축구"; if(intCat.equals(120124)) strCat="해외축구"; if(intCat.equals(120125)) strCat="농구"; if(intCat.equals(120126)) strCat="배구"; if(intCat.equals(120127)) strCat="골프"; if(intCat.equals(120128)) strCat="스포츠일반";
                    if(intCat.equals(130131)) strCat="국내연예"; if(intCat.equals(1301132)) strCat="해외연예";

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