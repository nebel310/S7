<script lang="ts" setup>
  const onUpload = () => {
    $toast.add({ severity: 'info', summary: 'Success', detail: 'Фото загружено', life: 3000 });
  }
</script>

<template>
      <div class="grid grid-nogutter surface-section text-800">

<!-- Section 1 -->
        <div class="col-12 md:col-12 p-2 text-center md:text-left flex align-items-center ">
      <div class="surface-section px-4 py-5 md:px-6 lg:px-8">
        <ul class="list-none p-0 m-0 flex align-items-center font-medium mb-3">
          <li>
            <a class="text-500 no-underline line-height-3 cursor-pointer">Начало карьеры</a>
          </li>
          <li class="px-2">
            <i class="pi pi-angle-right text-500 line-height-3" />
          </li>
          <li>
            <span class="text-900 line-height-3">О компании s7</span>
          </li>
        </ul>
        <div class="flex align-items-start flex-column lg:justify-content-between lg:flex-row">
          <div>
            <div class="font-medium text-3xl text-900 mb-2">
              Важная информация
            </div>
            <div class="flex align-items-left text-700 flex-column">

              <p>Добро пожаловать на первое вводное занятие.</p><br/>
			  <p>Начнём про рассказ об авиакомпании s7 и условиях работы...</p><br/>
			  <p>Особенности работы в профессии бортпроводниками...</p><br/>
            </div>			
            <div class="flex align-items-center text-700 flex-wrap mb-4">
              <div class="mr-5 flex align-items-center mt-3">
                <i class="pi pi-users mr-2" />
                <span>332 раза прочитано</span>
              </div>
              <div class="mr-5 flex align-items-center mt-3">

              </div>
              <div class="flex align-items-center mt-3">
                <i class="pi pi-clock mr-2" />
                <span>2.32м Время чтения</span>
              </div>
            </div>
          </div>
        </div>
          <div class="mt-3 lg:mt-0">
            <Button label="Я прочитал(а)" icon="pi pi-check" />
          </div>
      </div>
	</div>  
<!-- Section 2 -->
        <div class="col-12 md:col-12 p-2 text-center md:text-left flex align-items-center ">
      <div class="surface-section px-4 py-5 md:px-6 lg:px-8">
        <ul class="list-none p-0 m-0 flex align-items-center font-medium mb-3">
          <li>
            <a class="text-500 no-underline line-height-3 cursor-pointer">Начало карьеры</a>
          </li>
          <li class="px-2">
            <i class="pi pi-angle-right text-500 line-height-3" />
          </li>
          <li>
            <span class="text-900 line-height-3">Фотография</span>
          </li>
        </ul>
        <div class="flex align-items-start flex-column lg:justify-content-between lg:flex-row">
          <div>
            <div class="font-medium text-3xl text-900 mb-2">
              Загрузите фото
            </div>
            <div class="flex align-items-left text-700 flex-column">

              <p>Наша умная система помогает компании выбирать наилучших кандидатов.</p><br/>
			  <p>Заранее советуем - не пытайтесь обмануть или запутать систему. В дальнейшем после записи через приложение 
			  Вы будете очно оцениваться людьми в комиссии на собеседование куда Вы приедете...</p><br/>
			  <p>Подготовьте фото хорошего качества и загрузите...</p><br/>
			  <p>Результат обработки отобразится ниже...</p><br/>
          <div class="mt-3 lg:mt-0">
      <div class="card">
        <h5>Начните загружать</h5>
        <FileUpload
          name="demo[]"
          url="/upload.php"
          :multiple="true"
          accept="image/*"
          :max-file-size="1000000"
          @upload="onUpload"
        />
		</div>
          </div>			  
            </div>			
            <div class="flex align-items-center text-700 flex-wrap mb-4">
              <div class="mr-5 flex align-items-center mt-3">
                <i class="pi pi-users mr-2" />
                <span>1000 фото обработано</span>
              </div>
              <div class="mr-5 flex align-items-center mt-3">

              </div>
              <div class="flex align-items-center mt-3">
                <i class="pi pi-clock mr-2" />
                <span>15м. Время прохождения блока</span>
              </div>
            </div>
          </div>
        </div>
          <div class="mt-3 lg:mt-0">
            <Button label="Полетели дальше" icon="pi pi-check" />
          </div>
      </div>
    </div>

<!-- Section 3 -->
        <div class="col-12 md:col-12 p-2 text-center md:text-left flex align-items-center ">
      <div class="surface-section px-4 py-5 md:px-6 lg:px-8">
        <ul class="list-none p-0 m-0 flex align-items-center font-medium mb-3">
          <li>
            <a class="text-500 no-underline line-height-3 cursor-pointer">Начало карьеры</a>
          </li>
          <li class="px-2">
            <i class="pi pi-angle-right text-500 line-height-3" />
          </li>
          <li>
            <span class="text-900 line-height-3">Резюме</span>
          </li>
        </ul>
        <div class="flex align-items-start flex-column lg:justify-content-between lg:flex-row">
          <div>
            <div class="font-medium text-3xl text-900 mb-2">
              Загрузите резюме
            </div>
            <div class="flex align-items-left text-700 flex-column">
              <p>Загрузите своё резюме а перед этим посмотрите примеры наилучших кандидатов.</p><br/>
			  <p>Если Вы сомневаетесь в своих способностях составить резюме закажите составление резюме через Меню в разделе Наши услуги...</p><br/>
			  <p>Система займётся оценкой Ваших качеств. Результат обработки отобразится ниже...</p><br/>
          <div class="mt-3 lg:mt-0">
      <div class="card">
        <h5>Начните загружать</h5>
        <FileUpload
          name="demo[]"
          url="/upload.php"
          :multiple="true"
          accept="image/*"
          :max-file-size="1000000"
          @upload="onUpload"
        />
		</div>
          </div>			  
            </div>			
            <div class="flex align-items-center text-700 flex-wrap mb-4">
              <div class="mr-5 flex align-items-center mt-3">
                <i class="pi pi-users mr-2" />
                <span>1000 резюме обработано</span>
              </div>
              <div class="mr-5 flex align-items-center mt-3">

              </div>
              <div class="flex align-items-center mt-3">
                <i class="pi pi-clock mr-2" />
                <span>15м. Время прохождения блока</span>
              </div>
            </div>
          </div>
        </div>
          <div class="mt-3 lg:mt-0">
            <Button label="Полетели дальше" icon="pi pi-check" />
          </div>
      </div>
    </div>
<!-- Section 4 -->
<div class="surface-section px-4 py-8 md:px-6 lg:px-8">
    <div class="text-700 text-center">
        <div class="text-blue-600 font-bold mb-3"><i class="pi pi-discord"></i>&nbsp;ПОЗДРАВЛЕНИЯ ОТ S7</div>
        <div class="text-900 font-bold text-5xl mb-3">Спасибо Вы сумели пройти все испытания!</div>
        <div class="text-700 text-2xl mb-5">Скоро мы пришлём уведомление о результатах отбора. Внимательно проверяйте наши сообщения. Если Вы готовы сразу приступить к прохождению курсов нажмите на кнопку ниже</div>
        <Button label="Готов к курсам!" icon="pi pi-discord" class="font-bold px-5 py-3 p-button-raised p-button-rounded white-space-nowrap"></Button>
    </div>
</div>
<!-- End Section 4 -->
      </div>
</template>
