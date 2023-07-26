package edu.sungshin.newkey;

public class NewsData {
    String title;
    String content;
    String press;
    String date;

    public NewsData() {
    }

    public NewsData(String title, String content, String press, String date) {
        this.title = title;
        this.content = content;
        this.press = press;
        this.date = date;
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
}
