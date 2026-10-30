import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

import 'config.dart';

void main() {
  runApp(const VirtualLabApp());
}

class VirtualLabApp extends StatelessWidget {
  const VirtualLabApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Virtual Science Lab',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFF1E3A8A),
        useMaterial3: true,
      ),
      home: const LabWebView(),
    );
  }
}

class LabWebView extends StatefulWidget {
  const LabWebView({super.key});

  @override
  State<LabWebView> createState() => _LabWebViewState();
}

class _LabWebViewState extends State<LabWebView> {
  late final WebViewController _controller;
  late String _url;
  int _progress = 0;
  String? _error;

  @override
  void initState() {
    super.initState();
    _url = kLabUrl;
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(Colors.white)
      ..setNavigationDelegate(
        NavigationDelegate(
          onProgress: (value) => setState(() => _progress = value),
          onPageStarted: (_) => setState(() {
            _error = null;
            _progress = 0;
          }),
          onPageFinished: (_) => setState(() => _progress = 100),
          onWebResourceError: (error) {
            if (error.isForMainFrame ?? true) {
              setState(() => _error = error.description);
            }
          },
        ),
      )
      ..loadRequest(Uri.parse(_url));
  }

  Future<void> _reload() async {
    setState(() => _error = null);
    await _controller.loadRequest(Uri.parse(_url));
  }

  Future<void> _changeAddress() async {
    final input = TextEditingController(text: _url);
    final next = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Lab address'),
        content: TextField(
          controller: input,
          keyboardType: TextInputType.url,
          autocorrect: false,
          decoration: const InputDecoration(
            hintText: 'https://…',
            helperText: 'Use the Streamlit link or your school LAN address.',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, input.text.trim()),
            child: const Text('Open'),
          ),
        ],
      ),
    );
    if (next != null && next.isNotEmpty) {
      setState(() {
        _url = next;
        _error = null;
      });
      await _controller.loadRequest(Uri.parse(_url));
    }
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        if (await _controller.canGoBack()) {
          await _controller.goBack();
        } else {
          SystemNavigator.pop();
        }
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('🧪 Virtual Science Lab'),
          actions: [
            IconButton(
              tooltip: 'Reload',
              onPressed: _reload,
              icon: const Icon(Icons.refresh),
            ),
            IconButton(
              tooltip: 'Change lab address',
              onPressed: _changeAddress,
              icon: const Icon(Icons.link),
            ),
          ],
          bottom: _progress < 100
              ? PreferredSize(
                  preferredSize: const Size.fromHeight(3),
                  child: LinearProgressIndicator(value: _progress / 100),
                )
              : null,
        ),
        body: _error == null
            ? WebViewWidget(controller: _controller)
            : _ErrorView(
                message: _error!,
                url: _url,
                onRetry: _reload,
                onChangeAddress: _changeAddress,
              ),
      ),
    );
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({
    required this.message,
    required this.url,
    required this.onRetry,
    required this.onChangeAddress,
  });

  final String message;
  final String url;
  final VoidCallback onRetry;
  final VoidCallback onChangeAddress;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.wifi_off, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              'Could not reach the lab',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(url, textAlign: TextAlign.center),
            const SizedBox(height: 8),
            Text(
              message,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 20),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Try again'),
            ),
            TextButton(
              onPressed: onChangeAddress,
              child: const Text('Change lab address'),
            ),
          ],
        ),
      ),
    );
  }
}
