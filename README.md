# Certificate & Invoice Kit

A free Python tool that creates clean, professional PDF **certificates** and **invoices** from the command line.

Live page and samples: https://bayti-smart.github.io/certificate-invoice-kit/

## Quick start

```bash
pip install -r requirements.txt

python generator.py certificate --name "Jane Doe" --course "Python for Beginners" --out cert.pdf

python generator.py invoice --client "Acme Ltd" --seller "My Studio" \
  --items "Logo design:1:250" "Hosting (months):12:5" --tax 0.1 --out invoice.pdf
```

Items use the format `description:quantity:unit_price`.

## Samples

- [Sample certificate](docs/samples/sample-certificate.pdf)
- [Sample invoice](docs/samples/sample-invoice.pdf)

## Premium templates

More designs and ready-to-edit packs are coming soon.

## License

MIT
