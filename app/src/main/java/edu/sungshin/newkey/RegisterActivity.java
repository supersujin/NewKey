package edu.sungshin.newkey;

import androidx.appcompat.app.AppCompatActivity;

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

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class RegisterActivity extends AppCompatActivity {
    private FirebaseAuth mFirebaseAuth;
    private DatabaseReference mDatabaseRef;
    private EditText mEtEmail,mEtPwd;
    private Button mBtnRegister;
    SharedPreferences sharedpreferences;
    public static final String mypreference = "newkey";
    public static final String Email = "emailKey";
    public static final String PassWord = "passWordKey";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        mFirebaseAuth=FirebaseAuth.getInstance();
        mDatabaseRef= FirebaseDatabase.getInstance().getReference("newkey");
        sharedpreferences = getSharedPreferences(mypreference, Context.MODE_PRIVATE);

        InputFilter[] filters=new InputFilter[]{inputFilter};
        mEtEmail=findViewById(R.id.et_email);
        mEtEmail.setFilters(filters);
        mEtPwd=findViewById(R.id.et_pwd);
        mEtPwd.setFilters(filters);
        mBtnRegister=findViewById(R.id.btn_register);
        mBtnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String strEmail=mEtEmail.getText().toString();
                String strPwd=mEtPwd.getText().toString();

                mFirebaseAuth.createUserWithEmailAndPassword(strEmail,strPwd).addOnCompleteListener(RegisterActivity.this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(Task<AuthResult> task) {
                        if(task.isSuccessful()){
                            FirebaseUser firebaseUser=mFirebaseAuth.getCurrentUser();
                            UserAccount account=new UserAccount();
                            account.setIdToken(firebaseUser.getUid());
                            account.setEmailId(firebaseUser.getEmail());
                            account.setPassword(strPwd);

                            mDatabaseRef.child("UserAccount").child(firebaseUser.getUid()).setValue(account);

                            String e = account.getEmailId();
                            String p = account.getPassword();
                            SharedPreferences.Editor editor = sharedpreferences.edit();
                            editor.putString(Email, e);
                            editor.putString(PassWord, p);
                            editor.commit();

                            Toast.makeText(RegisterActivity.this,"회원가입에 성공하셨습니다",Toast.LENGTH_SHORT).show();
                            Intent intent=new Intent(RegisterActivity.this,CatActivity1.class);
                            startActivity(intent);
                            finish();
                        } else{
                            Toast.makeText(RegisterActivity.this,"회원가입에 실패하셨습니다",Toast.LENGTH_SHORT).show();
                        }
                    }
                });
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