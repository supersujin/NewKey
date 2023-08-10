package edu.sungshin.newkey;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.InputFilter;
import android.text.Spanned;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class LoginActivity extends AppCompatActivity {
    SharedPreferences sharedpreferences;
    public static final String mypreference = "newkey";
    public static final String Email = "emailKey";
    public static final String PassWord = "passWordKey";
    private FirebaseAuth mFirebaseAuth;
    private DatabaseReference mDatabaseRef;
    private EditText mEtEmail,mEtPwd;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mFirebaseAuth=FirebaseAuth.getInstance();
        mDatabaseRef= FirebaseDatabase.getInstance().getReference("newkey");
        sharedpreferences = getSharedPreferences(mypreference, Context.MODE_PRIVATE);

        InputFilter[] filters=new InputFilter[]{inputFilter};
        mEtEmail=findViewById(R.id.et_email);
        mEtEmail.setFilters(filters);
        mEtPwd=findViewById(R.id.et_pwd);
        mEtPwd.setFilters(filters);
        Button btn_login=findViewById(R.id.btn_login);
        btn_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //로그인 요청
                String strEmail=mEtEmail.getText().toString();
                String strPwd=mEtPwd.getText().toString();

                mFirebaseAuth.signInWithEmailAndPassword(strEmail,strPwd).addOnCompleteListener(LoginActivity.this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(Task<AuthResult> task) {
                        if(task.isSuccessful()){
                            String e = strEmail;
                            String p = strPwd;
                            SharedPreferences.Editor editor = sharedpreferences.edit();
                            editor.putString(Email, e);
                            editor.putString(PassWord, p);
                            editor.commit();

                            Intent intent=new Intent(LoginActivity.this,MainActivity.class);
                            startActivity(intent);
                            finish();
                        } else{
                            Toast.makeText(LoginActivity.this,"로그인 실패",Toast.LENGTH_SHORT).show();
                        }
                    }
                });
            }
        });

        Button btn_register=findViewById(R.id.btn_register);
        btn_register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //회원가입 화면으로 이동
                Intent intent=new Intent(LoginActivity.this,RegisterActivity.class);
                startActivity(intent);
            }
        });
    }

    InputFilter inputFilter=new InputFilter() {
        @Override
        public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
            if(source.toString().matches("^[0-9a-zA-Z@\\.\\_\\-]+$")){
                return source;
            }else{
                return "";
            }
        }
    };
}