package com.example.kennyd.robottts;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button testTalkButton = (Button)findViewById(R.id.testTalk);
        testTalkButton.setOnClickListener(this);
    }

    public void onClick(View v)
    {
        switch(v.getId())
        {
            case R.id.testTalk:
                testTalking();
                break;
        }
    }

    public void testTalking(){
        Log.v("**LOG**", "Button Pressed");
        Intent talkingRobot = new Intent(this, TestTalkActivity.class);
        startActivity(talkingRobot);
    }
}
