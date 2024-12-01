import { zodResolver } from "@hookform/resolvers/zod";
import "./App.css";
import { Controller, FormProvider, useForm } from "react-hook-form";
import z from "zod";
import { saveAs } from "file-saver";
import { useState } from "react";

const formSchema = z.object({
  course: z.string().min(1, "O campo é obrigatório"),
  matter: z.string().min(1, "O campo é obrigatório"),
  name: z.string().min(1, "O campo é obrigatório"),
  id: z.string().min(1, "O campo é obrigatório"),
  city: z.string().min(1, "O campo é obrigatório"),
});

type FormSchema = z.infer<typeof formSchema>;

type FormList = {
  label: string;
  name: keyof FormSchema;
};

const formList: FormList[] = [
  {
    label: "Curso",
    name: "course",
  },
  {
    label: "Matéria",
    name: "matter",
  },
  {
    label: "Nome",
    name: "name",
  },
  {
    label: "Identificação",
    name: "id",
  },
  {
    label: "Cidade",
    name: "city",
  },
];

type FetchStatus = "idle" | "loading" | "success" | "error";
function App() {
  const [pdf, setPdf] = useState<Blob | null>(null);
  const [fetchStatus, setFetchStatus] = useState<FetchStatus>("idle");

  const methods = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
  });

  const { handleSubmit, control } = methods;

  const onSubmit = async (data: FormSchema) => {
    setFetchStatus("loading");
    const res = await fetch("http://127.0.0.1:5000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      const pdfBlob = await res.blob();
      setTimeout(() => {
        setFetchStatus("success");
        setPdf(pdfBlob);

      },400);
    } else {
      setFetchStatus("error");
      console.error("Failed to generate PDF:", res.status);
    }
  };
  return (
    <FormProvider {...methods}>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-2 w-[400px] bg-gray-500/20 backdrop-blur shadow p-4 rounded-md "
      >
        <h1 className="text-xl text-start">Gerador Capa Uniube</h1>
        {formList.map((item, index) => (
          <Controller
            control={control}
            name={item.name}
            render={({ field, fieldState: { error } }) => (
              <div key={index} className="flex flex-col gap-1 items-start w-full">
                <label
                  htmlFor={item.name}
                  className={`${
                    error ? 'text-red-400 after:content-["*"]' : "text-white"
                  } text-sm`}
                >
                  {item.label}:
                </label>
                <input
                  type={"text"}
                  className="w-full py-2 px-4 border rounded-sm border-black/20 hover:ring-1 hover:ring-white/30 active:ring-1 active:ring-white/60"
                  {...field}
                />
                {error && (
                  <span className="text-xs text-red-400 font-bold">
                    {error.message}
                  </span>
                )}
              </div>
            )}
          />
        ))}
        <button type="submit" className="mt-2" disabled={fetchStatus === "loading"}>
          Gerar PDF
        </button>
        {fetchStatus === "loading" && <span>Gerando PDF...</span>}
        {pdf && fetchStatus === "success" && (
          <button onClick={() => saveAs(pdf, "capa.pdf")}>Download PDF</button>
        )}
      </form>
    </FormProvider>
  );
}

export default App;
