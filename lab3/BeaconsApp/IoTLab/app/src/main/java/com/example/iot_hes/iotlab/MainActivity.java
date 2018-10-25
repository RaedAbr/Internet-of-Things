package com.example.iot_hes.iotlab;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputFilter;
import android.text.Spanned;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.estimote.coresdk.common.config.EstimoteSDK;
import com.estimote.coresdk.common.requirements.SystemRequirementsChecker;
import com.estimote.coresdk.observation.region.beacon.BeaconRegion;
import com.estimote.coresdk.recognition.packets.Beacon;
import com.estimote.coresdk.service.BeaconManager;

import java.io.Console;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {

    TextView PositionText;
    EditText Percentage;
    Button   IncrButton;
    Button   DecrButton;
    Button   LightButton;
    Button   StoreButton;
    Button   RadiatorButton;

    private BeaconManager beaconManager;
    private BeaconRegion beaconRegion = new BeaconRegion("rooms", null, 30874, null);

    private HashMap<Integer, String> rooms = initRooms();

    private HashMap<Integer, String> initRooms(){
        HashMap<Integer, String> rooms = new HashMap<>();
        rooms.put(43216, "1");
        rooms.put(10279, "2");
        return rooms;
    }

    // In the "OnCreate" function below:
    // - TextView, EditText and Button elements are linked to their graphical parts (Done for you ;) )
    // - "OnClick" functions for Increment and Decrement Buttons are implemented (Done for you ;) )
    //
    // TODO List:
    // - Use the Estimote SDK to detect the closest Beacon and figure out the current Room
    //     --> See Estimote documentation:  https://github.com/Estimote/Android-SDK
    // - Set the PositionText with the Room name
    // - Implement the "OnClick" functions for LightButton, StoreButton and RadiatorButton


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        PositionText   =  findViewById(R.id.PositionText);
        Percentage     =  findViewById(R.id.Percentage);
        IncrButton     =  findViewById(R.id.IncrButton);
        DecrButton     =  findViewById(R.id.DecrButton);
        LightButton    =  findViewById(R.id.LightButton);
        StoreButton    =  findViewById(R.id.StoreButton);
        RadiatorButton =  findViewById(R.id.RadiatorButton);

        EstimoteSDK.initialize(getApplicationContext(), "", "");
        EstimoteSDK.enableDebugLogging(true);

        beaconManager = new BeaconManager(getApplicationContext());

        beaconManager.setRangingListener(new BeaconManager.BeaconRangingListener() {
            @Override
            public void onBeaconsDiscovered(BeaconRegion region, List<Beacon> list) {
                if (!list.isEmpty()) {
                    PositionText.setText(Integer.toString(list.size()));
                    Beacon nearestBeacon = list.get(0);
                    PositionText.setText("Room " + rooms.get(nearestBeacon.getMinor()));
                }
            }
        });


        // Only accept input values between 0 and 100
        Percentage.setFilters(new InputFilter[]{new InputFilterMinMax("0", "100")});

        IncrButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                int number = Integer.parseInt(Percentage.getText().toString());
                if (number<100) {
                    number++;
                    Log.d("IoTLab-Inc", String.format("%d",number));
                    Percentage.setText(String.format("%d",number));
                }
            }
        });

        DecrButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                int number = Integer.parseInt(Percentage.getText().toString());
                if (number>0) {
                    number--;
                    Log.d("IoTLab-Dec", String.format("%d",number));
                    Percentage.setText(String.format("%d",number));
                }
            }
        });









        LightButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {
                // TODO Send HTTP Request to command light
                Log.d("IoTLab", Percentage.getText().toString());
            }
        });



        StoreButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                // TODO Send HTTP Request to command store
                Log.d("IoTLab", Percentage.getText().toString());
            }
        });



        RadiatorButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                // TODO Send HTTP Request to command radiator
                Log.d("IoTLab", Percentage.getText().toString());
            }
        });


    }


    // You will be using "OnResume" and "OnPause" functions to resume and pause Beacons ranging (scanning)
    // See estimote documentation:  https://developer.estimote.com/android/tutorial/part-3-ranging-beacons/
    @Override
    protected void onResume() {
        super.onResume();
        SystemRequirementsChecker.checkWithDefaultDialogs(this);
        beaconManager.connect(new BeaconManager.ServiceReadyCallback() {
            @Override
            public void onServiceReady() {
                beaconManager.startRanging(beaconRegion);
            }
        });
    }


    @Override
    protected void onPause() {
        super.onPause();
        beaconManager.stopRanging(beaconRegion);
    }

}










// This class is used to filter input, you won't be using it.

class InputFilterMinMax implements InputFilter {
    private int min, max;

    public InputFilterMinMax(int min, int max) {
        this.min = min;
        this.max = max;
    }

    public InputFilterMinMax(String min, String max) {
        this.min = Integer.parseInt(min);
        this.max = Integer.parseInt(max);
    }

    @Override
    public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {
        try {
            int input = Integer.parseInt(dest.toString() + source.toString());
            if (isInRange(min, max, input))
                return null;
        } catch (NumberFormatException nfe) { }
        return "";
    }

    private boolean isInRange(int a, int b, int c) {
        return b > a ? c >= a && c <= b : c >= b && c <= a;
    }
}