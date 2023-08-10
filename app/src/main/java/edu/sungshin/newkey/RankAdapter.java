package edu.sungshin.newkey;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class RankAdapter extends RecyclerView.Adapter<RankAdapter.RankViewHolder> {

    private List<RankItem> rankItems;

    public RankAdapter(List<RankItem> rankItems) {
        this.rankItems = rankItems;
    }

    @Override
    public RankViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.fragment_visual_item, parent, false);
        return new RankViewHolder(view);
    }

    @Override
    public void onBindViewHolder(RankViewHolder holder, int position) {
        RankItem item = rankItems.get(position);
        holder.button.setText(item.getRank());
        holder.textView.setText(item.getContent());
    }

    @Override
    public int getItemCount() {
        return rankItems.size();
    }

    static class RankViewHolder extends RecyclerView.ViewHolder {
        Button button;
        TextView textView;

        RankViewHolder(View itemView) {
            super(itemView);
            button = itemView.findViewById(R.id.btm_1st);
            textView = itemView.findViewById(R.id.text_1st);
        }
    }
}
