# Deployment checklist

The code is pushed to <https://github.com/ugumar02-ui/virtual-science-lab>.
Two steps remain, and both need the owner's own login.

## 1. Permanent web link (Streamlit Community Cloud, free)

1. Open <https://share.streamlit.io> and sign in with **GitHub** (account `ugumar02-ui`).
2. Click **Create app** → **Deploy a public app from GitHub**.
3. Fill in:
   - Repository: `ugumar02-ui/virtual-science-lab`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: choose a subdomain, for example `aku-virtual-lab`
4. Click **Deploy**. The first build takes 2–4 minutes.
5. The app is live at `https://<subdomain>.streamlit.app`.

No secrets or environment variables are needed.

## 2. Android APK

A signed APK is already published in the
[v1.0.0 release](https://github.com/ugumar02-ui/virtual-science-lab/releases/download/v1.0.0/VirtualScienceLab-1.0.apk).
Inside the app, tap the 🔗 button and type the lab address; it is remembered.

To rebuild, `mobile/native-android/` is a plain Android WebView app (no Flutter, no NDK):

```bash
cd mobile/native-android
./gradlew assembleRelease
```

Output: `mobile/native-android/app/build/outputs/apk/release/app-release.apk`

Change `DEFAULT_URL` in `mobile/native-android/app/src/main/java/pk/akueb/virtualsciencelab/MainActivity.java`
to ship a different default address. `mobile/` also holds a Flutter wrapper if preferred;
that one needs the Android NDK.

## Temporary demo link

While the permanent app is being deployed, a tunnel can expose the local copy:

```bash
# terminal 1 — Streamlit without CORS/XSRF for the tunnel
.venv/bin/streamlit run app.py --server.port 8502 \
  --server.enableCORS false --server.enableXsrfProtection false

# terminal 2 — public HTTPS URL, no account needed
ssh -p 443 -R0:localhost:8502 a.pinggy.io
```

The URL printed by `ssh` works for 60 minutes and only while both terminals stay open.
Use it for a quick demo, not for the final submission.
