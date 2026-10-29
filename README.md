# Image Percentage F — earlier prototype

> Public experimental source: see [PUBLICATION.md](PUBLICATION.md) for actual checks, known defects, restored modules and operational limits. Earlier audit decisions are historical.

Небольшое desktop-приложение на Python для анализа PDF-файлов: извлекает изображения из документа, оценивает процент заполнения по альфа-каналу и сохраняет результаты в Excel.

## Статус аудита

Этот репозиторий выглядит как более ранний и узкий прототип линии `FillPercent`.

Canonical/current project: [`MilliganCo/fillpercent`](https://github.com/MilliganCo/fillpercent).

## Возможности

- выбор PDF через графическое окно;
- извлечение встроенных изображений через PyMuPDF;
- расчёт процента заполнения по прозрачности;
- сохранение статистики в `PDF_Analysis.xlsx`;
- защита от повторного добавления одного и того же файла.

## Решение

- Не делать отдельным публичным проектом, если `fillpercent` остаётся canonical.
- Можно удалить после full-history scan или оставить private как ранний прототип.
- Если нужен публичный вариант, объединить полезную alpha-channel логику в `fillpercent`.

## License recommendation

MIT только если публикуется как standalone учебная utility после проверки истории.
