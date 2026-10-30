package com.marconirodrigues.cinema

import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.drawable.Drawable
import android.provider.Settings
import java.text.Collator
import java.util.Locale

/** Item do dock: um app instalado ou um atalho do projetor. */
sealed class Entry {
    abstract val label: String
    abstract val subtitle: String
    abstract val accent: Int
    abstract val intent: Intent
    abstract val icon: Drawable

    class App(
        val pkg: String,
        override val label: String,
        override val subtitle: String,
        override val accent: Int,
        override val intent: Intent,
        override val icon: Drawable,
        val banner: Drawable?,
    ) : Entry()

    class Shortcut(
        override val label: String,
        override val subtitle: String,
        override val accent: Int,
        override val intent: Intent,
        override val icon: Drawable,
    ) : Entry()
}

object Apps {

    // Pacotes do sistema do HY300 Pro (ver config/proteger.txt na raiz do projeto)
    private const val PKG_HDMI = "com.softwinner.awlivetv"
    private const val PKG_IMAGE = "com.htc.magcubicos"
    private const val PKG_FOCUS = "com.hysd.vafocus"

    fun launchIntent(pm: PackageManager, pkg: String): Intent? =
        (pm.getLeanbackLaunchIntentForPackage(pkg) ?: pm.getLaunchIntentForPackage(pkg))
            ?.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

    /** Favoritos de res/values/favoritos.xml que estão instalados, na ordem configurada. */
    fun favorites(context: Context): List<Entry.App> {
        val pm = context.packageManager
        return context.resources.getStringArray(R.array.favoritos).mapNotNull { line ->
            val parts = line.split('|')
            val pkg = parts[0].trim()
            val intent = launchIntent(pm, pkg) ?: return@mapNotNull null
            val info = runCatching { pm.getApplicationInfo(pkg, 0) }.getOrNull() ?: return@mapNotNull null
            val icon = pm.getApplicationIcon(info)
            Entry.App(
                pkg = pkg,
                label = pm.getApplicationLabel(info).toString(),
                subtitle = parts.getOrNull(2)?.trim() ?: context.getString(R.string.app_sub_default),
                accent = parts.getOrNull(1)?.let { runCatching { Color.parseColor(it.trim()) }.getOrNull() }
                    ?: dominantColor(icon),
                intent = intent,
                icon = icon,
                banner = banner(pm, pkg, intent),
            )
        }
    }

    /** Todos os apps abríveis (Android TV e celular), sem duplicatas, em ordem alfabética. */
    fun all(context: Context): List<Entry.App> {
        val pm = context.packageManager
        val seen = HashSet<String>()
        val result = ArrayList<Entry.App>()
        for (category in listOf(Intent.CATEGORY_LEANBACK_LAUNCHER, Intent.CATEGORY_LAUNCHER)) {
            val query = Intent(Intent.ACTION_MAIN).addCategory(category)
            for (ri in pm.queryIntentActivities(query, 0)) {
                val pkg = ri.activityInfo.packageName
                if (pkg == context.packageName || !seen.add(pkg)) continue
                val intent = Intent(Intent.ACTION_MAIN).addCategory(category)
                    .setComponent(ComponentName(pkg, ri.activityInfo.name))
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                val icon = ri.loadIcon(pm)
                result += Entry.App(
                    pkg = pkg,
                    label = ri.loadLabel(pm).toString(),
                    subtitle = "",
                    accent = dominantColor(icon),
                    intent = intent,
                    icon = icon,
                    banner = null,
                )
            }
        }
        val collator = Collator.getInstance(Locale("pt", "BR"))
        return result.sortedWith { a, b -> collator.compare(a.label, b.label) }
    }

    /** Atalhos do projetor. Os que não existem neste firmware ficam de fora. */
    fun shortcuts(context: Context): List<Entry.Shortcut> {
        val pm = context.packageManager
        fun icon(res: Int) = context.getDrawable(res)!!
        fun color(res: Int) = context.getColor(res)
        val list = ArrayList<Entry.Shortcut>()

        (findActivity(pm, PKG_HDMI, "MainActivity") ?: launchIntent(pm, PKG_HDMI))?.let {
            list += Entry.Shortcut(context.getString(R.string.hdmi), context.getString(R.string.hdmi_sub),
                color(R.color.shortcut_hdmi), it, icon(R.drawable.ic_hdmi))
        }
        findActivity(pm, PKG_IMAGE, "Correction", "Keystone", "Trapezoid")?.let {
            list += Entry.Shortcut(context.getString(R.string.image), context.getString(R.string.image_sub),
                color(R.color.shortcut_image), it, icon(R.drawable.ic_image))
        }
        (findActivity(pm, PKG_FOCUS, "Focus") ?: launchIntent(pm, PKG_FOCUS))?.let {
            list += Entry.Shortcut(context.getString(R.string.focus), context.getString(R.string.focus_sub),
                color(R.color.shortcut_focus), it, icon(R.drawable.ic_focus))
        }
        list += Entry.Shortcut(context.getString(R.string.all_apps), context.getString(R.string.all_apps_sub),
            color(R.color.shortcut_apps), Intent(context, AllAppsActivity::class.java), icon(R.drawable.ic_apps))
        Intent(Settings.ACTION_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            .takeIf { it.resolveActivity(pm) != null }
            ?.let {
                list += Entry.Shortcut(context.getString(R.string.settings), context.getString(R.string.settings_sub),
                    color(R.color.shortcut_settings), it, icon(R.drawable.ic_settings))
            }
        return list
    }

    /** Procura uma activity exportada do pacote cujo nome contenha uma das palavras. */
    private fun findActivity(pm: PackageManager, pkg: String, vararg keywords: String): Intent? {
        val activities = runCatching { pm.getPackageInfo(pkg, PackageManager.GET_ACTIVITIES).activities }
            .getOrNull() ?: return null
        val match = activities.firstOrNull { a ->
            a.exported && keywords.any { a.name.contains(it, ignoreCase = true) }
        } ?: return null
        return Intent().setComponent(ComponentName(pkg, match.name)).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    }

    private fun banner(pm: PackageManager, pkg: String, intent: Intent): Drawable? =
        runCatching { intent.component?.let { pm.getActivityBanner(it) } ?: pm.getApplicationBanner(pkg) }
            .getOrNull()

    /** Cor média dos pixels mais saturados do ícone, usada quando o favorito não define cor. */
    fun dominantColor(icon: Drawable): Int {
        val size = 16
        val bmp = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888)
        icon.setBounds(0, 0, size, size)
        icon.draw(Canvas(bmp))
        var r = 0f; var g = 0f; var b = 0f; var weight = 0f
        val hsv = FloatArray(3)
        for (y in 0 until size) for (x in 0 until size) {
            val c = bmp.getPixel(x, y)
            if (Color.alpha(c) < 200) continue
            Color.colorToHSV(c, hsv)
            val w = hsv[1] * hsv[2] + 0.05f
            r += Color.red(c) * w; g += Color.green(c) * w; b += Color.blue(c) * w; weight += w
        }
        bmp.recycle()
        if (weight == 0f) return Color.rgb(94, 92, 230)
        return Color.rgb((r / weight).toInt(), (g / weight).toInt(), (b / weight).toInt())
    }
}
