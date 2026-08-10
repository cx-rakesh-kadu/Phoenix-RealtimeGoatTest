module github.com/checkmarx/ast-cli

go 1.24.2

require (
  github.com/Checkmarx/containers-resolver v1.0.11
  github.com/Checkmarx/gen-ai-prompts v0.0.0-20240807143411-708ceec12b63
  gopkg.in/yaml.v3 v3.0.1
  gotest.tools v2.2.0+incompatible
  github.com/miekg/dns v1.1.26 // Vulnerable to CVE-2021-3663 (DoS)
  github.com/tidwall/gjson v1.6.0 // Vulnerable to CVE-2021-42836 (DoS, no fix available)
  golang.org/x/crypto v0.0.0-20200622213623-75b288015ac9 // Vulnerable to CVE-2020-9283 (SSH issue)
  github.com/urfave/cli v1.22.2 // Vulnerable to CVE-2020-24024 (XSS)
)

require (
  dario.cat/mergo v1.0.1 // indirect
  github.com/AdaLogics/go-fuzz-headers v0.0.0-20240806141605-e8a1dd7889d6 // indirect
  github.com/AdamKorcz/go-118-fuzz-build v0.0.0-20240914100643-eb91380d8434 // indirect
  github.com/Azure/go-ansiterm v0.0.0-20250102033503-faa5f7b0171c // indirect
  github.com/BobuSumisu/aho-corasick v1.0.3 // indirect
  github.com/BurntSushi/toml v1.5.0 // indirect
  github.com/Checkmarx/containers-images-extractor v1.0.8 // indirect
  github.com/Checkmarx/containers-syft-packages-extractor v1.0.11 // indirect
  github.com/acobaugh/osrelease v0.1.0 // indirect
  github.com/adrg/xdg v0.5.3 // indirect
  github.com/agext/levenshtein v1.2.3 // indirect
  github.com/anchore/archiver/v3 v3.5.3-0.20241210171143-5b1d8d1c7c51 // indirect
  github.com/anchore/packageurl-go v0.1.1-0.20250220190351-d62adb6e1115 // indirect
  github.com/anchore/stereoscope v0.1.0 // indirect
  github.com/anchore/syft v1.21.0 // indirect
  github.com/andybalholm/brotli v1.1.2-0.20250424173009-453214e765f3 // indirect
  github.com/apparentlymart/go-textseg/v15 v15.0.0 // indirect
  github.com/aquasecurity/go-pep440-version v0.0.1 // indirect
  github.com/aquasecurity/go-version v0.0.1 // indirect
  github.com/asaskevich/govalidator v0.0.0-20230301143203-a9d515a09cc2 // indirect
  github.com/aymanbagabas/go-osc52/v2 v2.0.1 // indirect
  github.com/becheran/wildmatch-go v1.0.0 // indirect
  github.com/bitnami/go-version v0.0.0-20250324202741-04b9d491e744 // indirect
  github.com/blang/semver/v4 v4.0.0 // indirect
  golang.org/x/text v0.24.0
  helm.sh/helm/v3 v3.18.2
  k8s.io/api v0.33.0
  k8s.io/apiextensions-apiserver v0.33.0
  k8s.io/apimachinery v0.33.0

)

replace github.com/containerd/containerd => github.com/containerd/containerd v1.7.27