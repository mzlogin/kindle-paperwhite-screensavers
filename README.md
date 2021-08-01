# kindle-paperwhite-screensavers

适用于 Kindle Paperwhite 的屏保图片。

与 [kual-screensaver-sync](https://github.com/mzlogin/kual-screensaver-sync) 配合使用时，需要有以下文件结构：

```
├── meta.json
└── screensavers
    ├── bg_ss00.png
    ├── bg_ss01.png
    ├── bg_ss02.png
```

meta.json 文件里记录了 screensavers 里每个 png 文件的 md5 值，screensavers 文件夹里的内容有更改时，记得重新运行 `python3 meta-data-generator.py` 重新生成 meta.json 文件。
