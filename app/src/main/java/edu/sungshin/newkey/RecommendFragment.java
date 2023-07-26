package edu.sungshin.newkey;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.ArrayList;

public class RecommendFragment extends Fragment {

    ArrayList<NewsData> newsList;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        ViewGroup rootView=(ViewGroup) inflater.inflate(R.layout.fragment_recommend, container, false);
        newsList=new ArrayList<>();

        //Adapter
        LinearLayoutManager layoutManager=new LinearLayoutManager(getContext(),LinearLayoutManager.VERTICAL,false);
        RecyclerView recyclerView=rootView.findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(layoutManager);
        NewsAdapter adapter=new NewsAdapter(rootView.getContext(),newsList);

        adapter.addItem(new NewsData("13년간 '두물머리' 때문에 추진…양평고속도로 종점이 '양서면'이었던 이유","content1","press1","date1"));
        adapter.addItem(new NewsData("title2","content2","press2","date2"));
        adapter.addItem(new NewsData("title3","content3","press3","date3"));

        recyclerView.setAdapter(adapter);

        return rootView;
    }
}