package edu.sungshin.newkey;

import android.os.Parcel;
import android.os.Parcelable;

public class NewsData implements Parcelable {
    private String title;
    private String content;
    private String press;
    private String date;

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

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(title);
        dest.writeString(content);
        dest.writeString(press);
        dest.writeString(date);
    }

    // Parcelable 인터페이스 구현 메서드들
    // Creator 객체를 생성하는 역할
    public static final Creator<NewsData> CREATOR = new Creator<NewsData>() {
        @Override
        public NewsData createFromParcel(Parcel in) {
            return new NewsData(in);
        }

        @Override
        public NewsData[] newArray(int size) {
            return new NewsData[size];
        }
    };

    // Parcelable 인터페이스 구현 메서드들
    // Parcel로부터 객체를 생성하는 역할
    protected NewsData(Parcel in) {
        title = in.readString();
        content = in.readString();
        press = in.readString();
        date = in.readString();
    }

    @Override
    public int describeContents() {
        return 0;
    }
}
