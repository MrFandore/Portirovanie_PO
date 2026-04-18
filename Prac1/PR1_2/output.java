import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

public class TextProcessor {

    public static String readTxt(String file_path) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(file_path))) {
            return br.lines().reduce("", String::concat);
        }
    }

    public static String readDocx(String file_path) throws Exception {
        // Placeholder for docx reading logic
        throw new UnsupportedOperationException("Формат .docx не поддерживается напрямую. Пожалуйста, конвертируйте файл в .txt.");
    }

    public static String readPdf(String file_path) throws IOException {
        // Placeholder for pdf reading logic
        throw new UnsupportedOperationException("Формат .pdf не поддерживается напрямую. Пожалуйста, конвертируйте файл в .txt.");
    }

    public static String readDoc(String file_path) throws Exception {
        throw new UnsupportedOperationException("Формат .doc не поддерживается напрямую. Пожалуйста, конвертируйте файл в .txt.");
    }

    public static String readFile(String file_path) throws IOException, Exception {
        String ext = file_path.substring(file_path.lastIndexOf(".") + 1).toLowerCase();
        if (ext.equals("txt")) {
            return readTxt(file_path);
        } else if (ext.equals("docx")) {
            return readDocx(file_path);
        } else if (ext.equals("pdf")) {
            return readPdf(file_path);
        } else if (ext.equals("doc")) {
            throw new UnsupportedOperationException("Формат .doc не поддерживается напрямую. Пожалуйста, конвертируйте файл в .txt.");
        } else {
            throw new IllegalArgumentException("Неподдерживаемый формат: " + ext);
        }
    }

    public static String analyzeText(String text) {
        int char_count = text.length();
        int word_count = text.split("\\s+").length;
        int sentence_endings = 0;
        for (char c : text.toCharArray()) {
            if (c == '.' || c == '!' || c == '?') {
                sentence_endings++;
            }
        }
        if (!text.isEmpty() && !Character.isWhitespace(text.charAt(text.length() - 1))) {
            sentence_endings++;
        }
        if (sentence_endings < 1) {
            sentence_endings = 1;
        }
        return String.format("{\"characters\": %d, \"words\": %d, \"sentences\": %d}", char_count, word_count, sentence_endings);
    }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Использование: java TextProcessor <путь_к_файлу>");
            System.out.println("Поддерживаемые форматы: .txt, .docx, .pdf");
            return;
        }

        String file_path = args[0];
        try {
            String text = readFile(file_path);
            String stats = analyzeText(text);
            System.out.println("Файл: " + file_path);
            System.out.println(stats);
            // Показываем первые 200 символов текста
            System.out.print("\n--- Первые 200 символов текста ---\n");
            System.out.println(text.substring(0, Math.min(text.length(), 200)) + (text.length() > 200 ? "..." : ""));
        } catch (Exception e) {
            System.err.println("Ошибка: " + e.getMessage());
        }
    }
}