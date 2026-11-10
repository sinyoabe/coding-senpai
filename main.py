import http.server
import socketserver
import os
import subprocess

PORT = 5555

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/build-apk-local':
            content_length = int(self.headers['Content-Length'])
            
            # Ambil nama aplikasi dari Header X-App-Name
            app_name = self.headers.get('X-App-Name', 'Coding_Senpai_App')
            html_code = self.rfile.read(content_length).decode('utf-8')
            
            print(f"\n[BUILD] Menerima request kompilasi APK: '{app_name}'...")
            
            temp_html = "/tmp/input_user.html"
            output_apk = f"/tmp/{app_name}.apk"
            
            # Simpan HTML pengguna
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_code)
            
            # Eksekusi script converter di WSL
            script_path = os.path.join(os.getcwd(), "local_apk_builder.sh")
            process = subprocess.run([script_path, temp_html, output_apk], capture_output=True, text=True)
            
            if os.path.exists(output_apk) and os.path.getsize(output_apk) > 100000:
                print(f"[SUCCESS] File '{app_name}.apk' berhasil dibuat! Ukuran: {os.path.getsize(output_apk)} bytes")
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.android.package-archive')
                self.send_header('Content-Disposition', f'attachment; filename="{app_name}.apk"')
                self.end_headers()
                
                with open(output_apk, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                print(f"[ERROR] Build Gagal:\n{process.stdout}\n{process.stderr}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Gagal memproses APK di WSL.")
        else:
            super().do_POST()

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"[INFO] Server Converter WSL aktif di Port {PORT}")
    httpd.serve_forever()
