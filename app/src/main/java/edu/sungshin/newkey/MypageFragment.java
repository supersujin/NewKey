package edu.sungshin.newkey;

import android.content.Context;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
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
    Context context;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView=(ViewGroup) inflater.inflate(R.layout.fragment_mypage, container, false);
        FirebaseUser user = FirebaseAuth.getInstance().getCurrentUser();
        String userId = user.getUid();
        context = container.getContext();

        email=rootView.findViewById(R.id.userid);
        selCat=rootView.findViewById(R.id.sel_cat);
        viewNews=rootView.findViewById(R.id.view_news);
        logout=rootView.findViewById(R.id.logout);
        withdrawal=rootView.findViewById(R.id.withdrawal);

        //userId 서버로 전달
        selCat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                FragmentManager fragmentManager = ((AppCompatActivity) context).getSupportFragmentManager();
                FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                fragmentTransaction.replace(R.id.container, new SelCatFragment());
                fragmentTransaction.addToBackStack(null); // 뒤로 가기 버튼으로 이전 Fragment로 돌아갈 수 있도록 추가
                fragmentTransaction.commit();
            }
        });

        viewNews.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                FragmentManager fragmentManager = ((AppCompatActivity) context).getSupportFragmentManager();
                FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                fragmentTransaction.replace(R.id.container, new ViewNewsFragment());
                fragmentTransaction.addToBackStack(null); // 뒤로 가기 버튼으로 이전 Fragment로 돌아갈 수 있도록 추가
                fragmentTransaction.commit();
            }
        });

        return rootView;
    }
}
