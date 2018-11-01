package com.example.iot_hes.iotlab;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LoginActivity extends AppCompatActivity {

    AutoCompleteTextView Server;
    AutoCompleteTextView Name;
    EditText Password;
    Button Signin;

    static private RequestQueue queue = null;
    private RequestQueue getRequestQueue() {
        return queue != null ? queue : Volley.newRequestQueue(this);
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Server = findViewById(R.id.server_ip_port);
        Name = findViewById(R.id.name);
        Password =findViewById(R.id.password);
        Signin = findViewById(R.id.sign_in_button);

        Signin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String layerSupportAddr = Server.getText().toString();
                final String userName = Name.getText().toString();
                final String userPassword = Password.getText().toString();

                String url = "http://" + layerSupportAddr + "/resource";

                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest
                    (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

                        @Override
                        public void onResponse(JSONObject response) {
                            Intent intent = new Intent(LoginActivity.this, MainActivity.class);
                            intent.putExtra("data", response.toString());
                            startActivity(intent);
                        }
                    }, new Response.ErrorListener() {

                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Toast.makeText(LoginActivity.this, error.toString(), Toast.LENGTH_LONG).show();
                        }
                    }) {

                    @Override
                    public Map<String, String> getHeaders() throws AuthFailureError {
                        Map<String, String> headers = new HashMap<>();
                        String credentials = userName + ":" + userPassword;
                        String auth = "Basic "
                                + Base64.encodeToString(credentials.getBytes(), Base64.NO_WRAP);
                        headers.put("Content-Type", "application/json");
                        headers.put("Authorization", auth);
                        return headers;
                    }
                };

                getRequestQueue().add(jsonObjectRequest);
            }
        });
    }
}
