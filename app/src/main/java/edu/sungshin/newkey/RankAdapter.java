package edu.sungshin.newkey;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class RankAdapter extends RecyclerView.Adapter<RankAdapter.RankViewHolder> {

    private List<RankItem> items;

    Context context;

    public RankAdapter(Context context, ArrayList<RankItem> NewsList){ this.context=context; items=NewsList;}

    @Override
    public RankViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.fragment_visual_item, parent, false);
        return new RankViewHolder(view);
    }

    @Override
    public void onBindViewHolder(RankViewHolder holder, int position) {
        RankItem item = items.get(position); //클릭하면 대응되는 포지션의 랭크 아이템을 얻을 수 있음 -> rankfragment로 전달
        holder.setItem(item);
        holder.button.setText(item.getRank());
        holder.textView.setText(item.getContent());
        holder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                FragmentManager fragmentManager = ((AppCompatActivity) context).getSupportFragmentManager();
                FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction();
                fragmentTransaction.replace(R.id.container, new RankFragment(item));
                fragmentTransaction.addToBackStack(null); // 뒤로 가기 버튼으로 이전 Fragment로 돌아갈 수 있도록 추가
                fragmentTransaction.commit();
            }
        });
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    static class RankViewHolder extends RecyclerView.ViewHolder {
        Button button;
        TextView textView;

        RankViewHolder(View itemView) {
            super(itemView);
            button = itemView.findViewById(R.id.btn_rank);
            textView = itemView.findViewById(R.id.text_rank);
        }
        public void setItem(RankItem item){
            button.setText(item.getRank());
            textView.setText(item.getContent());
        }
    }
}