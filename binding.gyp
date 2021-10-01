{
  'conditions': [
    ['OS=="win"', {
      'variables': {
        'MAGICK_ROOT%': '<!(python get_regvalue.py)',
        # download the dll binary and check off for libraries and includes
        'OSX_VER%': "0",
      }
    }],
    ['OS=="mac"', {
      'variables': {
        # matches 11.9.X , 11.11 and outputs 11.9, 11.11, 11.11, 11.12, 11.13
        'OSX_VER%': "<!(sw_vers | grep 'ProductVersion:' | grep -o '11.[0-9]*')",
      }
    }, {
      'variables': {
        'OSX_VER%': "0",
      }
    }]
  ],
  "targets": [
    {
      "target_name": "imagemagick",
      "sources": [ "src/imagemagick.cc" ],
      'cflags!': [ '-fno-exceptions' ],
      'cflags_cc!': [ '-fno-exceptions' ],
      "include_dirs" : [
        "<!(node -e \"require('nan')\")"
      ],
      "conditions": [
        ['OS=="win"', {
          "libraries": [
            '-l<(MAGICK_ROOT)/lib/CORE_RL_magick_.lib',
            '-l<(MAGICK_ROOT)/lib/CORE_RL_Magick++_.lib',
            '-l<(MAGICK_ROOT)/lib/CORE_RL_wand_.lib',
          ],
          'include_dirs': [
            '<(MAGICK_ROOT)/include',
          ]
        }],
        ['OS=="win" and target_arch!="x64"', {
          'defines': [
            '_SSIZE_T_',
          ]
        }],
        ['OSX_VER == "11.9" or OSX_VER == "11.10" or OSX_VER == "11.11" or OSX_VER == "11.12" or OSX_VER == "11.13"', {
          'xcode_settings': {
            'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
            'OTHER_CFLAGS': [
              '<!@(pkg-config --cflags ImageMagick++)'
            ],
            'OTHER_CPLUSPLUSFLAGS' : [
              '<!@(pkg-config --cflags ImageMagick++)',
              '-std=c++11',
              '-stdlib=libc++',
            ],
            'OTHER_LDFLAGS': ['-stdlib=libc++'],
            'MACOSX_DEPLOYMENT_TARGET': '10.7', # -mmacosx-version-min=10.7
          },
          "libraries": [
             '<!@(pkg-config --libs ImageMagick++)',
          ],
          'cflags': [
            '<!@(pkg-config --cflags ImageMagick++)'
          ],
        }],
        ['OS=="mac"', {
          'xcode_settings': {
            'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
            'OTHER_CFLAGS': [
              '<!@(pkg-config --cflags ImageMagick++)'
            ]
          },
          "libraries": [
             '<!@(pkg-config --libs ImageMagick++)',
          ],
          'cflags': [
            '<!@(pkg-config --cflags ImageMagick++)'
          ],
        }],
        ['OS=="linux" or OS=="solaris" or OS=="freebsd"', { # not windows not mac
          "libraries": [
            '<!@(pkg-config --libs ImageMagick++)',
          ],
          'cflags': [
            '<!@(pkg-config --cflags ImageMagick++)'
          ],
        }]
      ]
    }]
  }
