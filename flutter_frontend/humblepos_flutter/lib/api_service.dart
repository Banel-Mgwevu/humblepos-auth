// api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Change this to your API URL
  // For Android emulator: http://10.0.2.2:5000
  // For iOS simulator: http://localhost:5000
  // For physical device: http://YOUR_COMPUTER_IP:5000
  static const String baseUrl = 'http://localhost:5000';

  /// Login user with email and password
  static Future<Map<String, dynamic>> login(
    String email,
    String password,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      );

      final data = jsonDecode(response.body);
      return data;
    } catch (e) {
      return {
        'success': false,
        'message': 'Connection error: ${e.toString()}',
      };
    }
  }

  /// Get current user details
  static Future<Map<String, dynamic>> getCurrentUser(String token) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/user/me'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      final data = jsonDecode(response.body);
      return data;
    } catch (e) {
      return {
        'success': false,
        'message': 'Connection error: ${e.toString()}',
      };
    }
  }

  /// Update user profile
  static Future<Map<String, dynamic>> updateProfile(
    String token,
    String firstName,
    String lastName,
  ) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/user/update'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'first_name': firstName,
          'last_name': lastName,
        }),
      );

      final data = jsonDecode(response.body);
      return data;
    } catch (e) {
      return {
        'success': false,
        'message': 'Connection error: ${e.toString()}',
      };
    }
  }
}

/*
=============================================================================
IMPORTANT: API URL Configuration
=============================================================================

Update the baseUrl above based on where you're running the app:

1. ANDROID EMULATOR:
   static const String baseUrl = 'http://10.0.2.2:5000';

2. iOS SIMULATOR:
   static const String baseUrl = 'http://localhost:5000';

3. PHYSICAL DEVICE (same network):
   - Find your computer's IP address:
     Windows: ipconfig
     macOS/Linux: ifconfig or ip addr
   - Use: static const String baseUrl = 'http://192.168.X.X:5000';

4. PRODUCTION:
   static const String baseUrl = 'https://your-api-domain.com';

=============================================================================
Make sure your Flask API is running:
python app.py
=============================================================================
*/