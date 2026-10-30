plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.marconirodrigues.cinema"
    compileSdk = 30

    defaultConfig {
        applicationId = "com.marconirodrigues.cinema"
        minSdk = 26
        targetSdk = 30
        versionCode = 1
        versionName = "0.1.0"
    }

    // Chave fixa versionada no repositório: assim cada nova versão instala por cima da anterior
    // (a chave de debug padrão muda a cada máquina/CI e obrigaria a desinstalar o launcher).
    signingConfigs {
        create("cinema") {
            storeFile = rootProject.file("keystore/cinema-debug.jks")
            storePassword = "android"
            keyAlias = "cinema"
            keyPassword = "android"
        }
    }

    buildTypes {
        debug {
            signingConfig = signingConfigs.getByName("cinema")
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
            signingConfig = signingConfigs.getByName("cinema")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}
