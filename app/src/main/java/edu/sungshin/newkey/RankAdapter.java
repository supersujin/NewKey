package edu.sungshin.newkey;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.content.Context;

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
        RankItem item = items.get(position);
        holder.setItem(item);
        holder.button.setText(item.getRank());
        holder.textView.setText(item.getContent());
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
