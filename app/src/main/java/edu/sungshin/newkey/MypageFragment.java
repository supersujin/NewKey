package edu.sungshin.newkey;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

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
