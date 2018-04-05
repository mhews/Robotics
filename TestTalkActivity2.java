package com.example.kennyd.robottts;

import android.Manifest;
import android.arch.lifecycle.ViewModelStoreOwner;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Message;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;

public class TestTalkActivity extends AppCompatActivity implements View.OnClickListener{
    EditText talkText;
    TTS tts;
    STT stt;
    private SpeechRecognizer mSpeechRecognizer;
    private Intent mSpeechRecognizerIntent;
    private boolean mIslistening;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test_talk);
        talkText = (EditText) findViewById(R.id.talkText);
        Button talkButton = (Button)findViewById(R.id.talkButton);
        mSpeechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        mSpeechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        mSpeechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        mSpeechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE,
                this.getPackageName());
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            this.requestPermissions(
                    new String[]{Manifest.permission.RECORD_AUDIO},
                    0);        }

        RecognitionListener listener = new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle params) {

            }

            @Override
            public void onBeginningOfSpeech() {

            }

            @Override
            public void onRmsChanged(float rmsdB) {

            }

            @Override
            public void onBufferReceived(byte[] buffer) {

            }

            @Override
            public void onEndOfSpeech() {
                Log.v("LOG", "HI");

            }

            @Override
            public void onError(int error) {
                mSpeechRecognizer.startListening(mSpeechRecognizerIntent);

            }

            @Override
            public void onResults(Bundle results) {
                ArrayList<String> result = results
                        .getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                talkText.setText(result.get(0), TextView.BufferType.EDITABLE);
                Log.v("LOG", result.get(0));

                mSpeechRecognizer.startListening(mSpeechRecognizerIntent);
//                new Thread(new Runnable() {
//                    public void run() {
//                        ArrayList<String> result = results
//                                .getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
//                        Log.v("LOG", result.get(0));
//                        mSpeechRecognizer.startListening(mSpeechRecognizerIntent);
//                    }
//                });
            }

            @Override
            public void onPartialResults(Bundle partialResults) {

            }

            @Override
            public void onEvent(int eventType, Bundle params) {

            }
        };

        mSpeechRecognizer.setRecognitionListener(listener);
        mSpeechRecognizer.startListening(mSpeechRecognizerIntent);
        talkButton.setOnClickListener(this);
        tts = new TTS(this);
        tts.start();

    }

    public void onClick(View v){
        Toast.makeText(this,"onClick", Toast.LENGTH_SHORT).show();
        switch(v.getId()){
            case R.id.talkButton:
                String input = talkText.getText().toString();
                Message sendMsg = tts.handler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("TT", input);
                sendMsg.setData(b);
                tts.handler.sendMessage(sendMsg);
                break;
        }
    }
}
