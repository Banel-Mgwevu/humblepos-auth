import 'package:flutter/material.dart';
import 'welcome_screen.dart';
import 'update_profile_screen.dart';

class UserDetailsScreen extends StatelessWidget {
  final String token;
  final Map<String, dynamic> user;

  const UserDetailsScreen({
    super.key,
    required this.token,
    required this.user,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          'USER DETAILS',
          style: TextStyle(
            color: Color(0xFF00FF00),
            fontWeight: FontWeight.w700,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: Color(0xFF00FF00)),
            onPressed: () {
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (context) => const WelcomeScreen()),
                (route) => false,
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 60,
                    height: 60,
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: const Color(0xFF00FF00),
                        width: 3,
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Container(width: 40, height: 40, color: const Color(0xFF00FF00)),
                ],
              ),
              const SizedBox(height: 40),

              _buildInfoRow(context, 'NAME',
                  '${user['first_name']} ${user['last_name']}'),
              const SizedBox(height: 24),
              _buildInfoRow(context, 'EMAIL', user['email']),
              const SizedBox(height: 24),
              _buildInfoRow(context, 'USER ID', user['id']),
              const SizedBox(height: 24),
              _buildInfoRow(context, 'LAST UPDATED', _formatDate(user['updated_at'])),
              const Spacer(),

              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => UpdateProfileScreen(
                        token: token,
                        currentFirstName: user['first_name'],
                        currentLastName: user['last_name'],
                      ),
                    ),
                  );
                },
                child: const Text('UPDATE PROFILE'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInfoRow(BuildContext context, String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: const Color(0xFF00FF00),
                fontWeight: FontWeight.w700,
              ),
        ),
        const SizedBox(height: 8),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            border: Border.all(color: const Color(0xFF00FF00), width: 2),
          ),
          child: Text(
            value,
            style: const TextStyle(color: Colors.white, fontSize: 16),
          ),
        ),
      ],
    );
  }

  String _formatDate(String? dateStr) {
    if (dateStr == null) return 'N/A';
    try {
      final date = DateTime.parse(dateStr);
      return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')} '
          '${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}';
    } catch (_) {
      return dateStr;
    }
  }
}
