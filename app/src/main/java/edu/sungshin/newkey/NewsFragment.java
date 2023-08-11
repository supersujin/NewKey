package edu.sungshin.newkey;

import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class NewsFragment extends Fragment {

    TextView summary;
    TextView title;
    TextView content;
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

        summary=rootView.findViewById(R.id.summary);
        title=rootView.findViewById(R.id.newsTitle);
        content=rootView.findViewById(R.id.newsContent);

        //summary.setText(newsData.getSummary());
        title.setText(newsData.getTitle());
        content.setText(newsData.getContent());

        return rootView;
    }
}