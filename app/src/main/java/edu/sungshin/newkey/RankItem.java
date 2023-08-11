package edu.sungshin.newkey;

public class RankItem {
    private String rank;
    private String content;

    public String getRank() {
        return rank;
    }

    public String getContent() {
        return content;
    }

    public void setRank(String rank) {
        this.rank = rank;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public RankItem() {
    }

    public RankItem(String rank,String content) {
        this.rank=rank;
        this.content=content;
    }
}
