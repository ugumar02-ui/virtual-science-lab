package pk.akueb.virtualsciencelab;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

/**
 * Thin WebView wrapper around the AKU-EB Virtual Science Lab.
 *
 * The default address can be overridden from the link button in the header and
 * is remembered in SharedPreferences.
 */
public class MainActivity extends Activity {

    private static final String DEFAULT_URL = "https://virtual-science-lab.streamlit.app";
    private static final String PREFS = "lab";
    private static final String KEY_URL = "url";

    private WebView web;
    private ProgressBar progress;
    private FrameLayout content;
    private LinearLayout errorView;
    private TextView errorText;
    private String url;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        url = prefs.getString(KEY_URL, DEFAULT_URL);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.WHITE);

        root.addView(buildHeader());

        progress = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progress.setMax(100);
        progress.setIndeterminate(false);
        root.addView(progress, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, dp(3)));

        content = new FrameLayout(this);
        root.addView(content, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        web = new WebView(this);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String address) {
                progress.setVisibility(View.GONE);
                showWebView();
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request,
                                        WebResourceError error) {
                if (request.isForMainFrame()) {
                    showError(String.valueOf(error.getDescription()));
                }
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                progress.setVisibility(newProgress < 100 ? View.VISIBLE : View.GONE);
                progress.setProgress(newProgress);
            }
        });

        content.addView(web, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

        errorView = buildErrorView();
        errorView.setVisibility(View.GONE);
        content.addView(errorView, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

        setContentView(root);
        load();
    }

    private View buildHeader() {
        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.HORIZONTAL);
        header.setGravity(Gravity.CENTER_VERTICAL);
        header.setBackgroundColor(Color.rgb(30, 58, 138));
        header.setPadding(dp(14), 0, dp(6), 0);

        TextView title = new TextView(this);
        title.setText("Virtual Science Lab");
        title.setTextColor(Color.WHITE);
        title.setTextSize(18);
        title.setSingleLine(true);
        header.addView(title, new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        Button reload = headerButton("\u21bb");
        reload.setOnClickListener(v -> load());
        header.addView(reload);

        Button address = headerButton("\u26ad");
        address.setOnClickListener(v -> changeAddress());
        header.addView(address);

        return header;
    }

    private Button headerButton(String text) {
        Button button = new Button(this);
        button.setText(text);
        button.setTextSize(18);
        button.setTextColor(Color.WHITE);
        button.setBackgroundColor(Color.TRANSPARENT);
        button.setPadding(dp(10), 0, dp(10), 0);
        button.setMinimumWidth(0);
        button.setMinWidth(0);
        button.setMinimumHeight(0);
        button.setMinHeight(0);
        return button;
    }

    private LinearLayout buildErrorView() {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setGravity(Gravity.CENTER);
        box.setBackgroundColor(Color.WHITE);
        box.setPadding(dp(28), dp(28), dp(28), dp(28));

        TextView heading = new TextView(this);
        heading.setText("Could not reach the lab");
        heading.setTextSize(20);
        heading.setGravity(Gravity.CENTER);
        box.addView(heading);

        errorText = new TextView(this);
        errorText.setTextSize(13);
        errorText.setGravity(Gravity.CENTER);
        errorText.setPadding(0, dp(10), 0, dp(18));
        box.addView(errorText);

        Button retry = new Button(this);
        retry.setText("Try again");
        retry.setOnClickListener(v -> load());
        box.addView(retry);

        Button change = new Button(this);
        change.setText("Change lab address");
        change.setOnClickListener(v -> changeAddress());
        box.addView(change);

        return box;
    }

    private void load() {
        errorView.setVisibility(View.GONE);
        web.setVisibility(View.VISIBLE);
        progress.setVisibility(View.VISIBLE);
        web.loadUrl(url);
    }

    private void showWebView() {
        web.setVisibility(View.VISIBLE);
        errorView.setVisibility(View.GONE);
    }

    private void showError(String message) {
        progress.setVisibility(View.GONE);
        web.setVisibility(View.GONE);
        errorView.setVisibility(View.VISIBLE);
        errorText.setText(url + "\n\n" + message);
    }

    private void changeAddress() {
        EditText input = new EditText(this);
        input.setInputType(InputType.TYPE_TEXT_VARIATION_URI);
        input.setText(url);
        input.setSelectAllOnFocus(true);

        new AlertDialog.Builder(this)
                .setTitle("Lab address")
                .setMessage("Streamlit link or school LAN address")
                .setView(input)
                .setNegativeButton("Cancel", null)
                .setPositiveButton("Open", (dialog, which) -> {
                    String next = input.getText().toString().trim();
                    if (next.isEmpty()) {
                        return;
                    }
                    if (!next.startsWith("http://") && !next.startsWith("https://")) {
                        next = "https://" + next;
                    }
                    url = next;
                    getSharedPreferences(PREFS, MODE_PRIVATE)
                            .edit().putString(KEY_URL, url).apply();
                    load();
                })
                .show();
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
