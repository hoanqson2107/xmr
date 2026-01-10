# To learn more about how to use Nix to configure your environment
# see: https://firebase.google.com/docs/studio/customize-workspace
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"
  
  # 1. Thêm Python 3 và Git vào danh sách packages
  packages = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.git
    pkgs.jdk21 # Giữ lại nếu bạn vẫn cần Java, nếu không có thể xóa
    pkgs.unzip
  ];

  # Sets environment variables in the workspace
  env = {};
  
  idx = {
    # Thêm extension Python để dễ code (giữ lại Dart nếu cần)
    extensions = [
      "ms-python.python"
      "Dart-Code.flutter"
      "Dart-Code.dart-code"
    ];

    workspace = {
      onCreate = { };
      
      # 2. Cấu hình lệnh chạy tự động khi khởi động
      onStart = {
        run-mcp = ''
          # Kiểm tra nếu thư mục chưa tồn tại thì mới Clone
          if [ ! -d "mcp" ]; then
            git clone https://github.com/mamaduck0011-dotcom/mcp.git
          fi
          
          # Truy cập thư mục
          cd mcp
          
          # Cài đặt thư viện nếu cần (tùy chọn, bỏ comment nếu repo có yêu cầu)
          # pip install -r requirements.txt || true
          
          # Chạy ứng dụng
          python3 app.py
        '';
      };
    };

    # Tắt preview Flutter vì bạn đang chạy Python console
    previews = {
      enable = false;
    };
  };
}
