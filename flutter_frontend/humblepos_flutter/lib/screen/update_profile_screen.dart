import 'package:flutter/material.dart';
import '../api_service.dart';

class UpdateProfileScreen extends StatefulWidget {
  final String token;
  final String currentFirstName;
  final String currentLastName;

  const UpdateProfileScreen({
    super.key,
    required this.token,
    required this.currentFirstName,
    required this.currentLastName,
  });

  @override
  State<UpdateProfileScreen> createState() => _UpdateProfileScreenState();
}

class _UpdateProfileScreenState extends State<UpdateProfileScreen> {
  late final TextEditingController _firstNameController;
  late final TextEditingController _lastNameController;
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;

  @override
  void initState() {
    super.initState();
    _firstNameController = TextEditingController(text: widget.currentFirstName);
    _lastNameController = TextEditingController(text: widget.currentLastName);
  }

  @override
  void dispose() {
    _firstNameController.dispose();
    _lastNameController.dispose();
    super.dispose();
  }

  Future<void> _updateProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _successMessage = null;
    });

    try {
      final response = await ApiService.updateProfile(
        widget.token,
        _firstNameController.text.trim(),
        _lastNameController.text.trim(),
      );

      if (!mounted) return;

      if (response['success'] == true) {
        setState(() => _successMessage = 'Profile updated successfully!');
        await Future.delayed(const Duration(seconds: 2));
        if (!mounted) return;
        Navigator.pop(context, response['user']);
      } else {
        setState(() => _errorMessage = response['message'] ?? 'Update failed');
      }
    } catch (_) {
      setState(() =>
          _errorMessage = 'Connection error. Check if server is running.');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF00FF00)),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('UPDATE\nPROFILE',
                    style: Theme.of(context).textTheme.headlineMedium),
                const SizedBox(height: 8),
                Container(width: 180, height: 3, color: const Color(0xFF00FF00)),
                const SizedBox(height: 48),

                TextFormField(
                  controller: _firstNameController,
                  style: const TextStyle(color: Colors.white),
                  decoration: const InputDecoration(
                    labelText: 'FIRST NAME',
                    hintText: 'enter first name',
                  ),
                  validator: (value) =>
                      value == null || value.isEmpty ? 'First name is required' : null,
                ),
                const SizedBox(height: 24),

                TextFormField(
                  controller: _lastNameController,
                  style: const TextStyle(color: Colors.white),
                  decoration: const InputDecoration(
                    labelText: 'LAST NAME',
                    hintText: 'enter last name',
                  ),
                  validator: (value) =>
                      value == null || value.isEmpty ? 'Last name is required' : null,
                ),
                const SizedBox(height: 16),

                if (_successMessage != null)
                  _buildMessageBox(
                      _successMessage!, const Color(0xFF00FF00), Icons.check_circle_outline),
                if (_errorMessage != null)
                  _buildMessageBox(_errorMessage!, Colors.red, Icons.error_outline),

                const SizedBox(height: 32),

                ElevatedButton(
                  onPressed: _isLoading ? null : _updateProfile,
                  child: _isLoading
                      ? const SizedBox(
                          height: 24,
                          width: 24,
                          child: CircularProgressIndicator(
                            color: Colors.black,
                            strokeWidth: 3,
                          ),
                        )
                      : const Text('UPDATE'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMessageBox(String message, Color color, IconData icon) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(border: Border.all(color: color, width: 2)),
      child: Row(
        children: [
          Icon(icon, color: color),
          const SizedBox(width: 12),
          Expanded(child: Text(message, style: TextStyle(color: color))),
        ],
      ),
    );
  }
}
