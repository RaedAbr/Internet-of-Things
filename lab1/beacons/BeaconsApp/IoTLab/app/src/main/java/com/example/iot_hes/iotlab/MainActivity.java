package com.example.iot_hes.iotlab;

import android.content.Intent;
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
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.estimote.coresdk.common.config.EstimoteSDK;
import com.estimote.coresdk.common.requirements.SystemRequirementsChecker;
import com.estimote.coresdk.observation.region.beacon.BeaconRegion;
import com.estimote.coresdk.recognition.packets.Beacon;
import com.estimote.coresdk.service.BeaconManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
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
    private BeaconRegion region;

    private static Map<Integer, String> rooms;
    static String currentRoom;
    String jsonData;
//    static {
//        Map<String, String> rooms = new HashMap<>();
//        rooms.put("43216", "1");
//        rooms.put("10279", "2");
//        ROOMS = Collections.unmodifiableMap(rooms);
//    }

    static private RequestQueue queue = null;
    private RequestQueue getRequestQueue() {
        return queue != null ? queue : Volley.newRequestQueue(this);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent intent = getIntent();
        jsonData = intent.getStringExtra("data");
        try {
            JSONObject jsonOb = new JSONObject(jsonData);
            JSONArray Jbeacons = jsonOb.getJSONArray("beacons");
            rooms = new HashMap<>();
            for (int i = 0; i < Jbeacons.length(); i++) {
                JSONObject beacon = (JSONObject) Jbeacons.get(i);
                Log.e("json", beacon.toString());
                rooms.put(Integer.valueOf(beacon.getString("minor")), beacon.getString("room"));
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        PositionText   =  findViewById(R.id.PositionText);
        Percentage     =  findViewById(R.id.Percentage);
        IncrButton     =  findViewById(R.id.IncrButton);
        DecrButton     =  findViewById(R.id.DecrButton);
        LightButton    =  findViewById(R.id.LightButton);
        StoreButton    =  findViewById(R.id.StoreButton);
        RadiatorButton =  findViewById(R.id.RadiatorButton);

        EstimoteSDK.initialize(getApplicationContext(), "", "");
        EstimoteSDK.enableDebugLogging(true);

        beaconManager = new BeaconManager(this);
        region = new BeaconRegion(
                "rooms",
                UUID.fromString("b9407f30-f5f8-466e-aff9-25556b57fe6d"),
                30874, null);

        beaconManager.setRangingListener(new BeaconManager.BeaconRangingListener() {
            @Override
            public void onBeaconsDiscovered(BeaconRegion region, List<Beacon> list) {
                if (!list.isEmpty()) {
                    PositionText.setText(Integer.toString(list.size()));
                    Beacon nearestBeacon = list.get(0);
                    currentRoom = rooms.get(nearestBeacon.getMinor());
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
                try {
                    JSONObject jsonOb = new JSONObject(jsonData);
                    JSONArray Jlights = jsonOb.getJSONArray("lights");
                    String selectedLight = "";
                    for (int i = 0; i < Jlights.length(); i++) {
                        JSONObject light = (JSONObject) Jlights.get(i);
                        if (light.getString("room").toString().equals(currentRoom)) {
                            selectedLight = light.getString("node");
                        }
                    }

                    ArrayList<String> urls = new ArrayList<>();
                    urls.add("http://192.168.2.1:5000/dimmers/set_level");
                    try {
                        JSONObject jsonBody = new JSONObject();
                        jsonBody.put("node_id", selectedLight);
                        jsonBody.put("value", MainActivity.this.Percentage.getText().toString());

                        sendPostRequest(urls, jsonBody, urls.size());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        StoreButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                // Send HTTP Request to command store
                Log.d("IoTLab", Percentage.getText().toString());

                try {
                    JSONObject jsonOb = new JSONObject(jsonData);
                    JSONArray Jblinds = jsonOb.getJSONArray("blinds");
                    ArrayList<String> urls = new ArrayList<>();
                    for (int i = 0; i < Jblinds.length(); i++) {
                        JSONObject blind = (JSONObject) Jblinds.get(i);
                        if (blind.getString("room").toString().equals(currentRoom)) {
                            String floor = blind.getString("floor");
                            String bloc = blind.getString("bloc");
                            urls.add("http://192.168.2.7:3002/blind/" + floor + "/" + bloc);
                        }
                    }

                    try {
                        Integer percentage = Integer.valueOf(MainActivity.this.Percentage.getText().toString());
                        JSONObject jsonBody = new JSONObject();
                        jsonBody.put("new_value", percentage * 255 / 100);

                        sendPostRequest(urls, jsonBody, urls.size());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

        RadiatorButton.setOnClickListener(new View.OnClickListener() {

            public void onClick(View v) {

                // Send HTTP Request to command radiator
                Log.e("IoTLab", Percentage.getText().toString());

                try {
                    JSONObject jsonOb = new JSONObject(jsonData);
                    JSONArray Jradiators = jsonOb.getJSONArray("radiators");
                    ArrayList<String> urls = new ArrayList<>();
                    for (int i = 0; i < Jradiators.length(); i++) {
                        JSONObject radiator = (JSONObject) Jradiators.get(i);
                        if (radiator.getString("room").toString().equals(currentRoom)) {
                            String floor = radiator.getString("floor");
                            String bloc = radiator.getString("bloc");
                            urls.add("http://192.168.2.7:3002/valve/" + floor + "/" + bloc);
                        }
                    }

                    try {
                        Integer percentage = Integer.valueOf(MainActivity.this.Percentage.getText().toString());
                        JSONObject jsonBody = new JSONObject();
                        jsonBody.put("new_value", percentage * 255 / 100);

                        sendPostRequest(urls, jsonBody, urls.size());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void sendPostRequest(final ArrayList<String> urls, final JSONObject jsonBody, final int repeat) {
        if (repeat == 0) {
            return;
        }
        final String mRequestBody = jsonBody.toString();

        StringRequest stringRequest = new StringRequest(Request.Method.POST, urls.get(repeat - 1), new Response.Listener<String>() {
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
                beaconManager.startRanging(region);
            }
        });
    }


    @Override
    protected void onPause() {
        beaconManager.stopRanging(region);
        super.onPause();
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