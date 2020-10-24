package com.example.illuminaze;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Toast;
import android.widget.ToggleButton;

public class MainActivity extends Activity {

    private Button gratButton;
    private ToggleButton serviceButton;

    public boolean enable() {
        if (!IlluminazeAccessibilityService.isRunning()) {
            return false;
        }

        return true;
    }

    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.home_screen);

        serviceButton =  (ToggleButton) findViewById(R.id.service_button);
        serviceButton.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(enable() == false) {
                    serviceButton.setChecked(false);
                    Toast toast = Toast.makeText(getApplicationContext(),
                            "Please enable service!",
                            Toast.LENGTH_SHORT);

                    toast.show();
                    startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS));
                }
                else {
                    serviceButton.setChecked(true);
                }
            }
        });

        Log.i("Here", "HERERERER");
        System.out.println("HEYO");




    }
}
