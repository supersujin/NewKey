package edu.sungshin.newkey;

import android.os.Parcel;
import android.os.Parcelable;

public class NewsData{
    private String id;
    private String title;
    private String content;
    private String press;
    private String date;
    private String img;
    private String summary;
    private String key;

    public NewsData() {
    }

    public NewsData(String id, String title, String content, String press, String date, String img, String summary, String key) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.press = press;
        this.date = date;
        this.img = img;
        this.summary = summary;
        this.key = key;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getPress() {
        return press;
    }

    public void setPress(String press) {
        this.press = press;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getImg() { return img; }

    public void setImg(String img) { this.img = img; }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }
}
