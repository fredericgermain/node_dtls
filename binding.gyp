{
  'variables': {
    # node v0.6.x doesn't give us its build variables,
    # but on Unix it was only possible to use the system OpenSSL library,
    # so default the variable to "true", v0.8.x node and up will overwrite it.
    'node_shared_openssl%': 'true'
  },
  'targets': [
    {
      'target_name': 'node_dtls',
      'sources': [
        'src/node_dtls.cc'
      ],
      
      'defines': [
        'NODE_WANT_INTERNALS=1',
        'ARCH="<(target_arch)"',
        'PLATFORM="<(OS)"',
      ],
      'link_settings': {
            'library_dirs': [
                              '/usr/local/opt/openssl/lib',
                              '/usr/lib',
                ],
                'libraries': [
                     '-lssl',
                ],
      },
 'conditions': [
        [ 'OS=="win"', {
          'conditions': [
            # "openssl_root" is the directory on Windows of the OpenSSL files
            ['target_arch=="x64"', {
              'variables': {
                'openssl_root%': 'C:/OpenSSL-Win64'
              },
            }, {
              'variables': {
                'openssl_root%': 'C:/OpenSSL-Win32'
              },
            }],
          ],
          'defines': [
            'uint=unsigned int',
          ],
          'libraries': [
            '-l<(openssl_root)/lib/libeay32.lib',
          ],
          'include_dirs': [
            '<(openssl_root)/include',
          ],
        }, { # OS!="win"
          
   'conditions': [
        ['node_shared_openssl=="false"', {
          # so when "node_shared_openssl" is "false", then OpenSSL has been
          # bundled into the node executable. So we need to include the same
          # header files that were used when building node.
          'include_dirs': [
            '<(node_root_dir)/deps/openssl/openssl/include'
          ],
          "conditions" : [
            ["target_arch=='ia32'", {
              "include_dirs": [ "<(node_root_dir)/deps/openssl/config/piii" ]
            }],
            ["target_arch=='x64'", {
              "include_dirs": [ "<(node_root_dir)/deps/openssl/config/k8" ]
            }],
            ["target_arch=='arm'", {
              "include_dirs": [ "<(node_root_dir)/deps/openssl/config/arm" ]
            }]
          ]
        }]

	],
        }],

      ]
    }
  ]
}
