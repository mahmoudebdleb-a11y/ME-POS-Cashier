from pathlib import Path

root=Path('build-src')
gradle=root/'app/build.gradle'
s=gradle.read_text(encoding='utf-8')
s=s.replace('versionCode 107','versionCode 108')
s=s.replace("versionName '1.0.7-client-images'","versionName '1.0.8-play-release'")
gradle.write_text(s,encoding='utf-8')
print('PLAY_RELEASE_108_APPLIED')
