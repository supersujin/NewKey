package edu.sungshin.newkey;

import java.util.ArrayList;

public class UserAccount {
    private String idToken;
    private String emailId;
    private String password;
    private ArrayList<String> select_cat;

    public UserAccount(){ }

    public String getIdToken() {
        return idToken;
    }

    public void setIdToken(String idToken) {
        this.idToken = idToken;
    }

    public String getEmailId() {
        return emailId;
    }

    public void setEmailId(String emailId) {
        this.emailId = emailId;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public ArrayList<String> getSelect_cat() {
        return select_cat;
    }

    public void setSelect_cat(ArrayList<String> select_cat) {
        this.select_cat = select_cat;
    }
}
