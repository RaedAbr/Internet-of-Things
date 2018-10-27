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

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.estimote.coresdk.common.config.EstimoteSDK;
import com.estimote.coresdk.common.requirements.SystemRequirementsChecker;
import com.estimote.coresdk.observation.region.beacon.BeaconRegion;
import com.estimote.coresdk.recognition.packets.Beacon;
import com.estimote.coresdk.service.BeaconManager;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.Console;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

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

    static private RequestQueue queue = null;
    private RequestQueue getRequestQueue() {
        return queue != null ? queue : Volley.newRequestQueue(this);
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
                    Log.e("IoTLab-Inc", String.format("%d",number));
                    Percentage.setText(String.format("%d",number));
                }
            }
        });

        DecrButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                int number = Integer.parseInt(Percentage.getText().toString());
                if (number>0) {
                    number--;
                    Log.e("IoTLab-Dec", String.format("%d",number));
                    Percentage.setText(String.format("%d",number));
                }
            }
        });






        LightButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {
                // Send HTTP Request to command light
                Log.e("IoTLab", Percentage.getText().toString());

                String[] urls = {"http://192.168.2.1:5000/dimmers/set_level"};
                try {
                    JSONObject jsonBody = new JSONObject();
                    jsonBody.put("node_id", "5");
                    jsonBody.put("value", MainActivity.this.Percentage.getText().toString());

                    sendPostRequest(urls, jsonBody, urls.length);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });



        StoreButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                // Send HTTP Request to command store
                Log.d("IoTLab", Percentage.getText().toString());

                String[] urls = {
                        "http://192.168.2.7:3002/blind/4/2",
                        "http://192.168.2.7:3002/blind/4/1"
                };

                try {
                    Integer percentage = Integer.valueOf(MainActivity.this.Percentage.getText().toString());
                    JSONObject jsonBody = new JSONObject();
                    jsonBody.put("new_value", percentage * 255 / 100);

                    sendPostRequest(urls, jsonBody, urls.length);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });



        RadiatorButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                // Send HTTP Request to command radiator
                Log.e("IoTLab", Percentage.getText().toString());

                String[] urls = {
                        "http://192.168.2.7:3002/valve/4/2",
                        "http://192.168.2.7:3002/valve/4/1"
                };

                try {
                    Integer percentage = Integer.valueOf(MainActivity.this.Percentage.getText().toString());
                    JSONObject jsonBody = new JSONObject();
                    jsonBody.put("new_value", percentage * 255 / 100);

                    sendPostRequest(urls, jsonBody, urls.length);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });


    }

    private void sendPostRequest(final String urls[], final JSONObject jsonBody, final int repeat) {
        if (repeat == 0) {
            return;
        }
        final String mRequestBody = jsonBody.toString();

        StringRequest stringRequest = new StringRequest(Request.Method.POST, urls[repeat - 1], new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.i("LOG_RESPONSE", response);
                sendPostRequest(urls, jsonBody, repeat - 1);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("LOG_RESPONSE", error.toString());
            }
        }) {
            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";
            }

            @Override
            public byte[] getBody() throws AuthFailureError {
                try {
                    return mRequestBody == null ? null : mRequestBody.getBytes("utf-8");
                } catch (UnsupportedEncodingException uee) {
                    VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s", mRequestBody, "utf-8");
                    return null;
                }
            }

            @Override
            protected Response<String> parseNetworkResponse(NetworkResponse response) {
                String responseString = "";
                if (response != null) {
                    responseString = String.valueOf(response.statusCode);
                }
                return Response.success(responseString, HttpHeaderParser.parseCacheHeaders(response));
            }
        };

        getRequestQueue().add(stringRequest);
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