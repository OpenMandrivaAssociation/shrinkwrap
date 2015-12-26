%{?_javapackages_macros:%_javapackages_macros}
%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}
Name:          shrinkwrap
Version:       1.1.2
Release:       3.1
Summary:       A simple mechanism to assemble Java archives
Group:		Development/Java
License:       ASL 2.0
Url:           http://www.jboss.org/shrinkwrap/
Source0:       https://github.com/shrinkwrap/shrinkwrap/archive/%{namedversion}.tar.gz
# remove env.JAVA"x"_HOME
# malformed pom file, not able to use pom macros
Patch0:        %{name}-%{namedversion}-remove-enforcer-requireProperty.patch

BuildRequires: java-devel
BuildRequires: mvn(org.jboss:jboss-parent:pom:)

BuildRequires: mvn(org.jboss.apiviz:apiviz)
BuildRequires: mvn(junit:junit)

BuildRequires: maven-local
BuildRequires: maven-checkstyle-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-source-plugin
BuildRequires: maven-surefire-provider-junit4

# required by enforcer-plugin
BuildRequires: mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires: mvn(org.apache.maven.shared:maven-shared-components:pom:)

BuildArch:     noarch

%description
Shrinkwrap provides a simple mechanism to assemble archives
like JARs, WARs, and EARs with a friendly, fluent API.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
%patch0 -p0

%pom_disable_module dist
# remove env.JAVA"x"_HOME
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-compiler-plugin']/pom:configuration/pom:executable"
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-surefire-plugin']/pom:configuration/pom:jvm" api
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-compiler-plugin']/pom:configuration/pom:executable" api-nio2
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-compiler-plugin']/pom:configuration/pom:executable" impl-nio2
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-surefire-plugin']/pom:configuration/pom:jvm" impl-base
%pom_xpath_remove "pom:profiles" impl-base 

sed -i 's/\r//' LICENSE

%mvn_file :%{name}-api %{name}/api
%mvn_file :%{name}-api-nio2 %{name}/api-nio2
%mvn_file :%{name}-build-resources %{name}/build-resources
%mvn_file :%{name}-impl-base %{name}/impl-base
%mvn_file :%{name}-impl-nio2 %{name}/impl-nio2
%mvn_file :%{name}-spi %{name}/spi

%build

%mvn_build

%install
%mvn_install

install -pm 644 api/target/%{name}-api-%{namedversion}-tests.jar %{buildroot}%{_javadir}/%{name}/api-tests.jar
install -pm 644 impl-base/target/%{name}-impl-base-%{namedversion}-tests.jar %{buildroot}%{_javadir}/%{name}/impl-base-tests.jar

%files -f .mfiles
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/api-tests.jar
%{_javadir}/%{name}/impl-base-tests.jar
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 gil cattaneo <puntogil@libero.it> 1.1.2-2
- build with XMvn
- minor changes to adapt to current guideline

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 1.1.2-1
- update to 1.1.2

* Tue Feb 19 2013 gil cattaneo <puntogil@libero.it> 1.0.0-5
- set java.home for enforcer-plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 gil cattaneo <puntogil@libero.it> 1.0.0-1
- initial rpm

