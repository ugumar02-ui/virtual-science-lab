plugins {
    id("com.android.application")
}

android {
    namespace = "pk.akueb.virtualsciencelab"
    compileSdk = 37

    defaultConfig {
        applicationId = "pk.akueb.virtualsciencelab"
        minSdk = 23
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
