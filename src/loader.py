from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

def load_pdf(data_path):
    loader = DirectoryLoader(
        path=data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    doc = loader.load()
    return doc

# print(load_pdf("../data"))