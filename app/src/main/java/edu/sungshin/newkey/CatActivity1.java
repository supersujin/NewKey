package edu.sungshin.newkey;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class CatActivity1 extends AppCompatActivity {
    private HashMap<String, Integer> catDict;
    private ArrayList<Integer> catList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cat1);

        catDict = new HashMap<>();
        catDict.put("pol1",100264); catDict.put("pol2",100265); catDict.put("pol3",100268); catDict.put("pol4",100266); catDict.put("pol5",100267); catDict.put("pol6",100269);
        catDict.put("eco1",101259); catDict.put("eco2",101258); catDict.put("eco3",101261); catDict.put("eco4",101771); catDict.put("eco5",101260); catDict.put("eco6",101262); catDict.put("eco7",101310); catDict.put("eco8",101263);
        catDict.put("soc1",102249); catDict.put("soc2",102250); catDict.put("soc3",102251); catDict.put("soc4",102254); catDict.put("soc5",102252); catDict.put("soc6",102596); catDict.put("soc5",102255); catDict.put("soc5",102256); catDict.put("soc7",102276); catDict.put("soc8",102257);
        catDict.put("lif1",103241); catDict.put("lif2",103239); catDict.put("lif3",103240); catDict.put("lif4",103237); catDict.put("lif5",103238); catDict.put("lif6",103376); catDict.put("lif7",103242); catDict.put("lif8",103243); catDict.put("lif9",103244); catDict.put("lif10",103248); catDict.put("lif11",103245);

        CheckBox pol1 = (CheckBox) findViewById(R.id.pol1);
        CheckBox pol2 = (CheckBox) findViewById(R.id.pol2);
        CheckBox pol3 = (CheckBox) findViewById(R.id.pol3);
        CheckBox pol4 = (CheckBox) findViewById(R.id.pol4);
        CheckBox pol5 = (CheckBox) findViewById(R.id.pol5);
        CheckBox pol6 = (CheckBox) findViewById(R.id.pol6);

        CheckBox eco1 = (CheckBox) findViewById(R.id.eco1);
        CheckBox eco2 = (CheckBox) findViewById(R.id.eco2);
        CheckBox eco3 = (CheckBox) findViewById(R.id.eco3);
        CheckBox eco4 = (CheckBox) findViewById(R.id.eco4);
        CheckBox eco5 = (CheckBox) findViewById(R.id.eco5);
        CheckBox eco6 = (CheckBox) findViewById(R.id.eco6);
        CheckBox eco7 = (CheckBox) findViewById(R.id.eco7);
        CheckBox eco8 = (CheckBox) findViewById(R.id.eco8);

        CheckBox soc1 = (CheckBox) findViewById(R.id.soc1);
        CheckBox soc2 = (CheckBox) findViewById(R.id.soc2);
        CheckBox soc3 = (CheckBox) findViewById(R.id.soc3);
        CheckBox soc4 = (CheckBox) findViewById(R.id.soc4);
        CheckBox soc5 = (CheckBox) findViewById(R.id.soc5);
        CheckBox soc6 = (CheckBox) findViewById(R.id.soc6);
        CheckBox soc7 = (CheckBox) findViewById(R.id.soc7);
        CheckBox soc8 = (CheckBox) findViewById(R.id.soc8);
        CheckBox soc9 = (CheckBox) findViewById(R.id.soc9);
        CheckBox soc10 = (CheckBox) findViewById(R.id.soc10);

        CheckBox lif1 = (CheckBox) findViewById(R.id.lif1);
        CheckBox lif2 = (CheckBox) findViewById(R.id.lif2);
        CheckBox lif3 = (CheckBox) findViewById(R.id.lif3);
        CheckBox lif4 = (CheckBox) findViewById(R.id.lif4);
        CheckBox lif5 = (CheckBox) findViewById(R.id.lif5);
        CheckBox lif6 = (CheckBox) findViewById(R.id.lif6);
        CheckBox lif7 = (CheckBox) findViewById(R.id.lif7);
        CheckBox lif8 = (CheckBox) findViewById(R.id.lif8);
        CheckBox lif9 = (CheckBox) findViewById(R.id.lif9);
        CheckBox lif10 = (CheckBox) findViewById(R.id.lif10);
        CheckBox lif11 = (CheckBox) findViewById(R.id.lif11);

        Button nextButton=findViewById(R.id.nextButton);
        catList=new ArrayList<>();

        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Set<String> keys = catDict.keySet();

                for (String key : keys) {
                    int resId = getResources().getIdentifier(key, "id", getPackageName());
                    CheckBox checkBox = findViewById(resId);

                    // Check if the CheckBox is checked
                    if (checkBox.isChecked()) {
                        Integer value = catDict.get(key);
                        catList.add(value);
                    }
                }

                Intent intent=new Intent(CatActivity1.this,CatActivity2.class);
                intent.putIntegerArrayListExtra("catList", catList);
                startActivity(intent);
                finish();
            }
        });
    }
}