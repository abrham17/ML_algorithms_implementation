import 'package:flutter/material.dart';
import 'config/theme.dart';
import 'features/auth/login_screen.dart';

void main() {
  runApp(const MFAApp());
}

class MFAApp extends StatelessWidget {
  const MFAApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Merchant Financial Agent',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      home: const LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
