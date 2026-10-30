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

The wrapper lives in `mobile/`. It opens the deployed URL inside a WebView.

```bash
cd mobile
flutter pub get
flutter build apk --release
```

Output: `mobile/build/app/outputs/flutter-apk/app-release.apk`

Set the permanent URL first in `mobile/lib/config.dart`:

```dart
const String kLabUrl = 'https://<subdomain>.streamlit.app';
```

Then rebuild. The APK is also usable without a rebuild: tap the link icon in the top bar
and type the lab address.

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
