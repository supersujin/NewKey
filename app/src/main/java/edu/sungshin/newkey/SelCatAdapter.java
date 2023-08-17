package edu.sungshin.newkey;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class SelCatAdapter extends RecyclerView.Adapter<SelCatAdapter.ViewHolder> {

    ArrayList<SelCat> items=new ArrayList<>();
    RequestQueue queue;
    Context context;

    public SelCatAdapter(Context context, ArrayList<SelCat> SelCatList){
        this.context=context;
        items=SelCatList;//생성자:전달한 comList 받아 items리스트에 대입
    }

    public void addItem(SelCat item){
        items.add(item);
    }
    public void setItems(ArrayList<SelCat> items){ this.items=items; }

    public SelCat getItem(int position){ return items.get(position); }

    public void setItem(int position, SelCat item){ items.set(position,item); }

    @Override
    public SelCatAdapter.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        LayoutInflater inflater=LayoutInflater.from(parent.getContext());
        View itemView=inflater.inflate(R.layout.selcat_item,parent,false);
        queue=Volley.newRequestQueue(context);

        return new ViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(SelCatAdapter.ViewHolder holder, int position) {
        SelCat item=items.get(position);
        holder.setItem(item);
    }

    @Override
    public int getItemCount() {
        return items.size();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView selCat;

        public ViewHolder(View itemView) {
            super(itemView);

            selCat=itemView.findViewById(R.id.sel_cat);
        }

        public void setItem(SelCat item){
            selCat.setText(item.getCat());
        }
    }
}