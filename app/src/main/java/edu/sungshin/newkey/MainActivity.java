package edu.sungshin.newkey;

import android.os.Bundle;
import android.view.WindowManager;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import com.google.android.material.tabs.TabLayout;

public class MainActivity extends AppCompatActivity {
    Toolbar toolbar;

    MainFragment mainFragment;
    RecommendFragment recommendFragment;
    VisualFragment visualFragment;
    MypageFragment mypageFragment;
    SearchFragment searchFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        mainFragment=new MainFragment();
        visualFragment=new VisualFragment();
        searchFragment=new SearchFragment();
        recommendFragment=new RecommendFragment();
        mypageFragment=new MypageFragment();

        toolbar=findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        ActionBar actionBar=getSupportActionBar();
        actionBar.setDisplayShowTitleEnabled(false);

        getSupportFragmentManager().beginTransaction().replace(R.id.container,visualFragment).commit();

        TabLayout tabs = findViewById(R.id.tabs);
        tabs.addTab(tabs.newTab().setText("시각화"));
        tabs.addTab(tabs.newTab().setText("검색"));
        tabs.addTab(tabs.newTab().setText("뉴스"));
        tabs.addTab(tabs.newTab().setText("추천 뉴스"));
        tabs.addTab(tabs.newTab().setText("마이 페이지"));

        tabs.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                int position=tab.getPosition();

                if(position==0){
                    getSupportFragmentManager().beginTransaction().replace(R.id.container,visualFragment).commit();
                }else if(position==1){
                    getSupportFragmentManager().beginTransaction().replace(R.id.container,searchFragment).commit();
                }else if(position==2){
                    getSupportFragmentManager().beginTransaction().replace(R.id.container,mainFragment).commit();
                }else if(position==3){
                    getSupportFragmentManager().beginTransaction().replace(R.id.container,recommendFragment).commit();
                }else if(position==4){
                    getSupportFragmentManager().beginTransaction().replace(R.id.container,mypageFragment).commit();
                }
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {

            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {

            }
        });
    }
}