import 'package:flutter_test/flutter_test.dart';
import 'package:virtual_science_lab/config.dart';

void main() {
  test('the lab address is a full https URL', () {
    final uri = Uri.parse(kLabUrl);
    expect(uri.isScheme('https'), isTrue);
    expect(uri.host, isNotEmpty);
  });
}
